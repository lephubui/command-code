#include <iostream>
#include <bitset> // For displaying binary representation

int main() {
    int a = 12; // Binary: 00001100
    int b = 25; // Binary: 00011001

    std::cout << "a in binary: " << std::bitset<8>(a) << std::endl;
    std::cout << "b in binary: " << std::bitset<8>(b) << std::endl;

    // Bitwise AND (&)
    // Result: 00001000 (decimal 8)
    int result_and = a & b;
    std::cout << "a & b: " << std::bitset<8>(result_and) << " (decimal: " << result_and << ")" << std::endl;

    // Bitwise OR (|)
    // Result: 00011101 (decimal 29)
    int result_or = a | b;
    std::cout << "a | b: " << std::bitset<8>(result_or) << " (decimal: " << result_or << ")" << std::endl;

    // Bitwise XOR (^)
    // Result: 00010101 (decimal 21)
    int result_xor = a ^ b;
    std::cout << "a ^ b: " << std::bitset<8>(result_xor) << " (decimal: " << result_xor << ")" << std::endl;

    // Bitwise NOT (~)
    // For 'a' (00001100), the complement flips all bits.
    // The actual decimal value depends on the integer size and signedness.
    // For an 8-bit unsigned int, it would be 11110011 (decimal 243).
    // For a signed int, it's typically represented using two's complement.
    int result_not_a = ~a;
    std::cout << "~a: " << std::bitset<8>(result_not_a) << " (decimal: " << result_not_a << ")" << std::endl;

    // Left Shift (<<)
    // Shifting 'a' (00001100) left by 2 positions: 00110000 (decimal 48)
    int result_left_shift = a << 2;
    std::cout << "a << 2: " << std::bitset<8>(result_left_shift) << " (decimal: " << result_left_shift << ")" << std::endl;

    // Right Shift (>>)
    // Shifting 'b' (00011001) right by 1 position: 00001100 (decimal 12)
    int result_right_shift = b >> 1;
    std::cout << "b >> 1: " << std::bitset<8>(result_right_shift) << " (decimal: " << result_right_shift << ")" << std::endl;

    return 0;
}