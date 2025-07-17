#ifndef LISTEN_FOR_SYSLOGS_H
#define LISTEN_FOR_SYSLOGS_H

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

struct syslog {
    time_t received;
    struct in_addr address;
    unsigned int severity;
    unsigned int facility;
    time_t timestamp;
    char host[65];
    char tag[33];
    char msg[1024];
};

// Callback function to handle syslogs.
// Takes the struct syslog by value, to simplify ownership issues.
typedef void (*syslog_handler)(struct syslog syslog, void *data);

struct syslog_context {
    volatile int listening;
    int sock;
    syslog_handler handler;
    void *data;
};

// Takes a socket file descriptor, which must already be bound to an address and
// ready to receive data, and a syslog handler callback function to which it
// will pass any syslogs it receives. Doesn’t return until
// stop_listening_for_syslogs has been called (asynchronously).
void listen_for_syslogs(struct syslog_context *ctx);

// After this has been called, listen_for_syslogs will return.
void stop_listening_for_syslogs(struct syslog_context *ctx);

#endif // LISTEN_FOR_SYSLOGS_H
