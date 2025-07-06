# A RFC 3164 Syslog Server for testing

## Installation

    make
    make install

Uses PREFIX and DESTDIR to control installation location.

## Library

Installs a shared library, `libsyslog.so`, that provides functions to listen and to stop listening for syslogs.

## Server

Installs an application linked against `libsyslog.so`, that listens for syslogs and prints them out to standard out.

### Usage

    syslog <address> <port>

### Note

    Run under Ubuntu 24.04.2 LTS environment