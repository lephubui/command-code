.PHONY: all install clean

include config.mk

BINDIR = $(PREFIX)/bin
LIBDIR = $(PREFIX)/lib
LIBFILE = libs$(LIBRARY).so

all: $(EXECUTABLE) $(LIBFILE)

CFLAGS += -Wall -Wextra -Werror -fpic
LDFLAGS += -L. -l$(LIBRARY)

BIN_SOURCES = syslog.c

$(EXECUTABLE): $(BIN_SOURCES) $(LIBFILE)
	$(CC) $(CPPFLAGS) $(CFLAGS) -o $(EXECUTABLE) $(BIN_SOURCES) $(LDFLAGS)

LIB_SOURCES = listen_for_syslogs.c

$(LIBFILE): $(LIB_SOURCES)
	$(CC) $(CPPFLAGS) $(CFLAGS) -shared -o $(LIBFILE) $(LIB_SOURCES)

clean:
	rm -f $(EXECUTABLE) $(LIBFILE)

install: $(EXECUTABLE) $(LIBRARY)
	mkdir -p $(DESTDIR)$(BINDIR)
	mkdir -p $(DESTDIR)$(LIBDIR)
	install -m 0755 $(EXECUTABLE) $(DESTDIR)$(BINDIR)
	install -m 0755 $(LIBFILE) $(DESTDIR)$(LIBDIR)
