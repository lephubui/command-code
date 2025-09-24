#include <cstdint>
#include <iostream>
#include <iomanip>

// create mask of 'width' low bits (width in [0..32])
uint32_t make_mask(unsigned width) {
    if (width == 0) return 0u;
    if (width >= 32) return 0xFFFFFFFFu;
    // safer construction avoiding out-of-range left shift:
    return static_cast<uint32_t>(0xFFFFFFFFu >> (32 - width));
}

// extract inclusive field [hi:lo] from reg (right-aligned)
uint32_t extract_field(uint32_t reg, unsigned hi, unsigned lo) {
    if (hi < lo || hi >= 32 || lo >= 32) return 0u;
    unsigned width = hi - lo + 1;
    uint32_t mask = make_mask(width);
    return (reg >> lo) & mask;
}

// insert val into inclusive field [hi:lo] in reg without touching other bits
uint32_t insert_field(uint32_t reg, unsigned hi, unsigned lo, uint32_t val) {
    if (hi < lo || hi >= 32 || lo >= 32) return reg;
    unsigned width = hi - lo + 1;
    uint32_t mask = make_mask(width);
    uint32_t cleared = reg & ~(mask << lo);
    uint32_t v = (val & mask) << lo;
    return cleared | v;
}

// demo
int main() {
    uint32_t reg = 0xABCD1234u;
    uint32_t fld = extract_field(reg, 15, 8); // expect 0x12
    std::cout << "reg = 0x" << std::hex << std::setw(8) << std::setfill('0') << reg
              << "  [15:8] = 0x" << fld << " (" << std::dec << fld << ")\n";

    uint32_t newreg = insert_field(reg, 23, 16, 0xFFu);
    std::cout << "insert 0xFF into [23:16]: 0x" << std::hex << std::setw(8) << std::setfill('0') << newreg << "\n";

    return 0;
}