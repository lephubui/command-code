#include "listen_for_syslogs.h"
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <time.h>
#include "config.h"

char const * const SEVERITY[] = {
    "EMERGENCY", "ALERT", "CRITICAL", "ERROR", "WARNING", "NOTICE",
    "INFORMATIONAL", "DEBUG"
};

char const * const FACILITY[] = {
    "KERNEL", "USER", "MAIL", "SYSTEM", "SECURITY",
    "SYSLOG", "NETWORK", "UUCP", "CLOCK", "SECURITY/AUTH",
    "FTP", "NTP", "LOG-AUDIT", "LOG-ALERT", "CLOCK",
    "LOCAL 0", "LOCAL 1", "LOCAL 2", "LOCAL 3", "LOCAL 4",
    "LOCAL 5", "LOCAL 6", "LOCAL 7", "UNKNOWN"
};

// A syslog handler that formats and prints the syslog.
void print_syslog(struct syslog syslog, void *data)
{
    (void)data; // This handler doesn't make use of the data parameter.

    char received[64];
    char timestamp[64];

    strftime(
        received, sizeof(received), "%Y-%m-%d %H:%M:%S",
        localtime(&syslog.received)
    );

    strftime(
        timestamp, sizeof(timestamp), "%Y-%m-%d %H:%M:%S",
        localtime(&syslog.timestamp)
    );

    printf("[%s <- %s] %s %s[%s]: %s\n",
        received,
        inet_ntoa(syslog.addr),
        syslog.severity >= (sizeof(SEVERITY) / sizeof(SEVERITY[0])) ?
            SEVERITY[sizeof(SEVERITY) / sizeof(SEVERITY[0]) - 1] :
            SEVERITY[syslog.severity],
        syslog.facility >= (sizeof(FACILITY) / sizeof(FACILITY[0])) ?
            FACILITY[sizeof(FACILITY) / sizeof(FACILITY[0]) - 1] :
            FACILITY[syslog.facility],
        timestamp,
        syslog.host,
        syslog.tag,
        syslog.msg
    );

    fflush(stdout);
}

int main(int argc, char **argv)
{
    int sock;
    struct sockaddr_in server_address;
    int r;

    // Validate and parse the command line arguments.
    if(argc != 3) {
        printf("%s - %s\n", argv[0], VERSION);
        printf("Usage: %s <address> <port>\n", argv[0]);
        return 4;
    }

    char const *address = argv[1];
    unsigned int const port = atoi(argv[2]);

    // Get a socket.
    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if(sock < 0) {
        perror("socket");
        return 3;
    }

    // Bind the socket to the server address.
    memset(&server_address, 0, sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = inet_addr(address);
    server_address.sin_port = htons(port);

    r = bind(
        sock,
        (struct sockaddr const *)&server_address,
        sizeof(server_address)
    );
    if(r < 0) {
        perror("bind");
        return 1;
    }

    // Never returns.
    struct syslog_context ctx;
    ctx.sock = sock;
    ctx.handler = print_syslog;
    ctx.data = NULL;
    listen_for_syslogs(&ctx);

    // We never get here, but if we did, we'd clean up.
    r = close(sock);
    if(r < 0) {
        perror("close");
        return 2;
    }

    return 0;
}
