# Traffic Flooding Tools in C++

This project contains a set of raw socket-based traffic flooding tools written in C++ for network testing and simulation. The tools include:

- `arp_flood.cpp`: Sends ARP request floods with randomized source MACs.
- `snmp_flood.cpp`: Sends SNMP GET requests in a continuous loop to a target IP.
- `lldp_flood.cpp`: (Assuming this file is similar) Sends crafted LLDP packets to flood the network with discovery frames.
- `send_packets.cpp`: (Optional) General packet sender using raw sockets.

⚠️ **WARNING**: These tools generate high volumes of network traffic and should only be used in a controlled lab environment or with proper authorization. Misuse on production or public networks can result in serious consequences.

---

## 🖥️ Execution Environment

These tools are tested and built on:

- **Operating System**: Ubuntu 24.04.2 LTS
- **Compiler**: GCC 13 or later (C++17 standard)
- **Build System**: Meson + Ninja

---

## 🔧 Build Instructions

This project uses [Meson](https://mesonbuild.com/) as the build system and [Ninja](https://ninja-build.org/) as the backend.

### Prerequisites

- C++ compiler (GCC or Clang) with C++17 support
- `meson` and `ninja` packages installed
- Root privileges to run the executables

### Build Steps

```bash
# Set up the build directory
meson setup build

# Compile the project
meson compile -C build
