#include <cstdint>
#include <iostream>
#include <limits>

// Return 1 if number of set bits in 32-bit x is odd, else 0.
// XOR-folding method: repeatedly fold halves until single-bit parity remains.
int parity32(uint32_t x) noexcept {
    x ^= x >> 16;
    x ^= x >> 8;
    x ^= x >> 4;
    x ^= x >> 2;
    x ^= x >> 1;
    return static_cast<int>(x & 1u);
}

// 64-bit variant
int parity64(uint64_t x) noexcept {
    x ^= x >> 32;
    x ^= x >> 16;
    x ^= x >> 8;
    x ^= x >> 4;
    x ^= x >> 2;
    x ^= x >> 1;
    return static_cast<int>(x & 1ull);
}

int main() {
    // tests
    uint32_t a = 0u;                    // 0 bits set -> parity 0
    uint32_t b = 1u;                    // 1 bit set -> parity 1
    uint32_t c = 11u;                   // 1011b -> 3 bits set -> parity 1
    uint32_t d = std::numeric_limits<uint32_t>::max(); // 32 bits set -> parity 0

    std::cout << "parity32(0) = " << parity32(a) << '\n';
    std::cout << "parity32(1) = " << parity32(b) << '\n';
    std::cout << "parity32(11) = " << parity32(c) << '\n';
    std::cout << "parity32(UINT32_MAX) = " << parity32(d) << '\n';

    // 64-bit example
    uint64_t e = std::numeric_limits<uint64_t>::max(); // 64 bits set -> parity 0
    std::cout << "parity64(UINT64_MAX) = " << parity64(e) << '\n';

    return 0;
}