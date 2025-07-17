#define _XOPEN_SOURCE
#include <sys/types.h>
#include <sys/socket.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <errno.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <ctype.h>
#include <time.h>

#include "listen_for_syslogs.h"

// For parsing timestamps from received syslogs.
static char const * const MONTHS[] = {
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
};

// Trim leading and trailing whitespace.
static char *trim(char *str)
{
    // Remove leading whitespace
    while (isspace(*str)) str++;

    // Find the last non-whitespace character
    char *last_non_ws = str;
    char *ptr = str;
    while (*ptr != '\0') {
        if (!isspace(*ptr)) {
            last_non_ws = ptr;
        }
        ptr++;
    }

    // Remove trailing whitespace
    char *end = (last_non_ws + 1);
    *end = '\0';

    return str;
}

// Custom character predicates
static int isab(int c) {
    return (c == '<') || (c == '>');
}

static int iscolon(int c) {
    return c == ':';
}

static int isnotalnum(int c) {
    return !isalnum(c);
}

static int isnotascii(int c) {
    return !isascii(c);
}

// Token parser
static char const *get_token(
    char *out, size_t t_outl,
    char const *in,
    int (*leading)(int), int (*valid)(int), int (*delim)(int))
{
    char const *out_end = out + t_outl - 1;

    while (leading(*in)) in++;

    while (valid(*in) && !delim(*in) && (out < out_end)) {
        *out++ = *in++;
    }
    *out = '\0';

    if (!delim(*in)) return NULL;
    return in;
}

// Main syslog listener
void listen_for_syslogs(struct syslog_context *ctx)
{
    socklen_t length;
    struct syslog syslog;
    int bytes_received;
    struct sockaddr_in client_address;
    struct tm timestamp;
    char buffer[1025];

    ctx->listening = 1;
    while (ctx->listening) {
        // Receive a syslog
        memset(&syslog, 0, sizeof(syslog));
        memset(&client_address, 0, sizeof(client_address));
        length = sizeof(client_address);
        bytes_received = recvfrom(
            ctx->sock,
            buffer,
            sizeof(buffer) - 1,
            MSG_WAITALL,
            (struct sockaddr *)&client_address,
            &length
        );

        if (bytes_received < 0) {
            continue;
        }

        buffer[bytes_received] = 0;

        // Parse the syslog
        char pri[4] = "", timestr[33] = "";
        char month[4] = "", day[3] = "", hour[3] = "", minute[3] = "", second[3] = "";
        char host[65] = "", tag[33] = "", msg[1024] = "";

        char const *buffer_p = buffer;
        buffer_p = get_token(pri, sizeof(pri), buffer_p, isab, isdigit, isab);
        if (buffer_p == NULL) continue;

        if (isalpha(buffer_p[1])) {
            buffer_p = get_token(month, sizeof(month), buffer_p, isab, isalpha, isspace);
            if (buffer_p == NULL) continue;

            buffer_p = get_token(day, sizeof(day), buffer_p, isspace, isdigit, isspace);
            if (buffer_p == NULL) continue;

            buffer_p = get_token(hour, sizeof(hour), buffer_p, isspace, isdigit, iscolon);
            if (buffer_p == NULL) continue;

            buffer_p = get_token(minute, sizeof(minute), buffer_p, iscolon, isdigit, iscolon);
            if (buffer_p == NULL) continue;

            buffer_p = get_token(second, sizeof(second), buffer_p, iscolon, isdigit, isspace);
            if (buffer_p == NULL) continue;
        } else if (isdigit(buffer_p[1])) {
            buffer_p = get_token(timestr, sizeof(timestr), buffer_p, isab, isascii, isspace);
            if (buffer_p == NULL) continue;
        } else {
            continue;
        }

        buffer_p = get_token(host, sizeof(host), buffer_p, isspace, isascii, isspace);
        if (buffer_p == NULL) continue;

        buffer_p = get_token(tag, sizeof(tag), buffer_p, isspace, isalnum, isnotalnum);
        if (buffer_p == NULL) continue;

        buffer_p = get_token(msg, sizeof(msg), buffer_p, isnotascii, isascii, isnotascii);
        if (buffer_p == NULL) continue;

        // Put the client's address in the struct.
        syslog.address = client_address.sin_addr;

        // Put the trimmed host, tag, and message strings into the struct.
        strncpy(syslog.host, trim(host), sizeof(syslog.host));
        strncpy(syslog.tag, trim(tag), sizeof(syslog.tag));
        strncpy(syslog.msg, trim(msg), sizeof(syslog.msg));

        // Parse the priority.
        int pri_i = atoi(pri);
        syslog.severity = pri_i % 8;
        syslog.facility = pri_i / 8;

        // Parse the timestamp.
        time_t now = time(NULL);
        memset(&timestamp, 0, sizeof(timestamp));
        if (strlen(timestr) == 0) {
            size_t month_i = 0;
            for (month_i = 0; month_i < sizeof(MONTHS)/sizeof(MONTHS[0]); month_i++) {
                if (strncmp(month, MONTHS[month_i], 3) == 0) {
                    break;
                }
            }

            timestamp.tm_mon = month_i;
            timestamp.tm_mday = atoi(day);
            timestamp.tm_hour = atoi(hour);
            timestamp.tm_min = atoi(minute);
            timestamp.tm_sec = atoi(second);
            timestamp.tm_year = localtime(&now)->tm_year; // current year
            timestamp.tm_isdst = -1;
        } else {
            char *rc = strptime(timestr, "%Y-%m-%dT%H:%M:%SZ", &timestamp);
            if (rc == NULL) continue;
        }

        syslog.received = now;                    // Local time we received it
        syslog.timestamp = mktime(&timestamp);    // Parsed timestamp

        // Hand it off to the user-defined handler
        ctx->handler(syslog, ctx->data);
    }
}

void stop_listening_for_syslogs(struct syslog_context *ctx)
{
    ctx->listening = 0;
}
