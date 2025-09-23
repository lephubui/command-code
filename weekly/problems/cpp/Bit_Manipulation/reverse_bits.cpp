#include <iostream>
#include <cstdint>
#include <limits>
#include <bitset>
#include <vector>

// Reverse bits (32-bit) - constant-time mask & shift method
uint32_t reverseBits(uint32_t n) {
    // swap odd and even bits
    n = ((n >> 1) & 0x55555555u) | ((n & 0x55555555u) << 1);
    // swap consecutive pairs
    n = ((n >> 2) & 0x33333333u) | ((n & 0x33333333u) << 2);
    // swap nibbles
    n = ((n >> 4) & 0x0F0F0F0Fu) | ((n & 0x0F0F0F0Fu) << 4);
    // swap bytes
    n = ((n >> 8) & 0x00FF00FFu) | ((n & 0x00FF00FFu) << 8);
    // swap 16-bit halves
    return (n >> 16) | (n << 16);
}

/* Demo for reverseBits */
void reverseBitsDemo() {
    uint32_t examples[] = { 2u, 0x00000001u, 0x80000000u, 0xF0F0000Fu };
    for (uint32_t v : examples) {
        uint32_t r = reverseBits(v);
        std::cout << "orig: " << std::bitset<32>(v)
                  << " -> rev: " << std::bitset<32>(r)
                  << " (" << r << ")\n";
    }
    std::cout << "----\n";
}

int main() {

    // demonstrate reverseBits
    reverseBitsDemo();
    std::cout << "Bit of 11 is: " << std::bitset<8>(11) << std::endl;
    return 0;
}