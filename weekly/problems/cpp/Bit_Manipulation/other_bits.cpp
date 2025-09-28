#include <cstdint>
#include <bitset>
#include <iostream>

int main() {
    uint8_t x = 0;              // 00000000
    x |= (1u << 7);            // set bit index 7 -> 10000000
    std::cout << std::bitset<8>(x) << " (" << +x << ")\n";
    return 0;
}