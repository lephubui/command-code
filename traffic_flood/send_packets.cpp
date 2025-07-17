#include <string>
#include <vector>
#include <regex>
#include <optional>
#include <functional>
#include <chrono>
#include <thread>
#include <random>
#include <cstdint>
#include <cstdlib>
#include <cstdio>
#include <sys/ioctl.h>
#include <net/if.h>
#include <unistd.h>
#include <linux/if_packet.h>

struct mac_addr {
    uint8_t mac[6];
};

[[noreturn]]
static void usage() {
    printf("Usage: send_packets "
           "-i <interface> "
           "[-w <minimum wait between packets (sec)>] "
           "[-W <maximum wait between packets (sec)>] "
           "[-c <total count of packets to send>] "
           "[-d <dest addr>] "
           "[-S <src addr>] "
           "[-l <payload length>] "
           "[-p <pcp priority>] "
           "[-v <vlan id>] "
           "\n");
    exit(1);
}

static mac_addr get_mac(int sock, char const* interface) {
    struct ifreq ifr{};
    snprintf(ifr.ifr_name, sizeof(ifr.ifr_name), "%s", interface);
    if (ioctl(sock, SIOCGIFHWADDR, &ifr) == -1) {
        fprintf(stderr, "ioctl(SIOCGIFHWADDR) failed for interface %s: %s\n",
                interface, strerror(errno));
        exit(1);
    }

    mac_addr result{};
    memcpy(result.mac, ifr.ifr_hwaddr.sa_data, 6u);
    return result;
}

static mac_addr read_mac(char const* input) {
    using std::regex_constants::icase;
    using std::regex_constants::extended;

    std::regex re("([0-9a-f]{2}):"
                  "([0-9a-f]{2}):"
                  "([0-9a-f]{2}):"
                  "([0-9a-f]{2}):"
                  "([0-9a-f]{2}):"
                  "([0-9a-f]{2})", icase | extended);

    std::cmatch match;
    if (!std::regex_match(input, match, re)) {
        fprintf(stderr, "invalid mac address: %s\n", input);
        exit(1);
    }

    mac_addr result{};
    for (int i = 0; i < 6; ++i) {
        auto value = std::stoul(match[i + 1].str(), nullptr, 16);
        result.mac[i] = value;
    }
    return result;
}

class RandomWait {
public:
    template <typename T>
    using duration = std::chrono::duration<T>;
    using nanoseconds = std::chrono::nanoseconds;
    using dist_type = std::uniform_int_distribution<nanoseconds::rep>;

    RandomWait(duration<double> min_wait, duration<double> max_wait) {
        using std::chrono::round;
        auto min = round<nanoseconds>(min_wait);
        auto max = round<nanoseconds>(max_wait);
        m_dist = dist_type(min.count(), max.count());
        std::random_device rd;
        m_rng.seed(rd());
    }

    void operator()() {
        auto const sleep_time = nanoseconds(m_dist(m_rng));
        std::this_thread::sleep_for(sleep_time);
    }

private:
    dist_type m_dist;
    std::mt19937 m_rng;
};

int main(int argc, char** argv) {
    // Parameters
    std::string interface;
    std::optional<std::chrono::duration<double>> wait_time;
    std::optional<std::chrono::duration<double>> max_wait_time;
    std::optional<unsigned long long> packet_count;
    mac_addr dest = {{1, 0xaa, 0xaa, 0xaa, 0xaa, 0xaa}};
    std::optional<mac_addr> src_addr;
    unsigned long size = 1500;
    unsigned long priority = 0;
    unsigned long vid = 0;

    // Parse options:
    int opt;
    while ((opt = getopt(argc, argv, "i:w:W:c:d:S:l:p:v:")) != -1) {
        switch (opt) {
        case 'i':
            interface = optarg;
            break;
        case 'w':
            wait_time = std::chrono::duration<double>(std::stod(optarg));
            if (*wait_time < std::chrono::duration<double>::zero()) {
                fprintf(stderr, "Wait time must be >= 0.\n");
                exit(1);
            }
            break;
        case 'W':
            max_wait_time = std::chrono::duration<double>(std::stod(optarg));
            if (*max_wait_time < std::chrono::duration<double>::zero()) {
                fprintf(stderr, "Max wait time must be >= 0.\n");
                exit(1);
            }
            break;
        case 'c':
            packet_count = std::stoull(optarg);
            break;
        case 'd':
            dest = read_mac(optarg);
            break;
        case 'S':
            src_addr = read_mac(optarg);
            break;
        case 'l':
            size = std::stoul(optarg);
            if (size > 1500) {
                fprintf(stderr, "payload size cannot be more than 1500\n");
                exit(1);
            }
            break;
        case 'p':
            priority = std::stoul(optarg);
            if (priority > 7) {
                fprintf(stderr, "invalid PCP priority value\n");
                exit(1);
            }
            break;
        case 'v':
            vid = std::stoul(optarg);
            if (vid > 4095) {
                fprintf(stderr, "invalid vlan id\n");
                exit(1);
            }
            break;
        }
    }

    if (interface.empty()) {
        fprintf(stderr, "interface is required\n");
        usage();
    }

    std::function<void()> wait;

    if (!wait_time && !max_wait_time) {
        wait = []() {};
    } else if (wait_time && !max_wait_time) {
        wait = [=]() { std::this_thread::sleep_for(*wait_time); };
    } else {
        if (!wait_time)
            wait_time = std::chrono::duration<double>::zero();
        if (*wait_time >= *max_wait_time) {
            fprintf(stderr, "Min wait time must be < max wait time\n");
            exit(1);
        }
        wait = RandomWait(*wait_time, *max_wait_time);
    }

    // Create a socket
    int sock = socket(AF_PACKET, SOCK_RAW, 0);
    if (sock == -1) {
        fprintf(stderr, "failed to create packet socket: %s\n", strerror(errno));
        exit(1);
    }

    if (!src_addr) {
        src_addr = get_mac(sock, interface.c_str());
    }

    std::vector<uint8_t> packet;
    packet.reserve(1518u);
    for (int i = 0; i < 6; ++i) packet.push_back(dest.mac[i]);
    for (int i = 0; i < 6; ++i) packet.push_back(src_addr->mac[i]);

    if (priority != 0 || vid != 0) {
        packet.push_back(0x81);
        packet.push_back(0x00);
        packet.push_back(((priority & 0x7) << 5) | ((vid >> 8) & 0x1F));
        packet.push_back(vid & 0xFF);
    }

    packet.push_back(0xCC);
    packet.push_back(0xCC);
    for (decltype(size) i = 0; i < size; ++i) packet.push_back(0);

    sockaddr_ll ll_addr{};
    ll_addr.sll_family = AF_PACKET;
    ll_addr.sll_ifindex = if_nametoindex(interface.c_str());
    if (ll_addr.sll_ifindex == 0) {
        fprintf(stderr, "invalid interface %s: %s\n", interface.c_str(), strerror(errno));
        exit(1);
    }

    auto addr = reinterpret_cast<sockaddr*>(&ll_addr);
    unsigned long long packets_sent = 0;

    while (!packet_count || packets_sent < *packet_count) {
        if (packets_sent > 0 && wait) {
            wait();
        }

        auto rc = sendto(sock, packet.data(), packet.size(), 0, addr, sizeof(ll_addr));
        if (rc == -1) {
            fprintf(stderr, "failed to send: %s\n", strerror(errno));
        }

        ++packets_sent;
    }

    return 0;
}
