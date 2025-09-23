#include <iostream>
#include <cstdint>
#include <limits>
#include <vector>

// Set count using Brian Kernighan's algorithm 32-bit integer
uint32_t countSetBits(uint32_t n) {
    // Brian Kernighan's algorithm: repeatedly clear the lowest set bit
    uint32_t count = 0;
    while (n) {
        n &= (n - 1);
        ++count;
    }
    return count;
}

int main() {
    std::vector<uint32_t> tests = {
        11u,                    // 1011b -> 3
        0u,                     // -> 0
        std::numeric_limits<uint32_t>::max() // all 32 bits set -> 32
    };

    for (uint32_t t : tests) {
        std::cout << "n=" << t << " -> set bits = " << countSetBits(t) << "\n";
    }

    return 0;
}