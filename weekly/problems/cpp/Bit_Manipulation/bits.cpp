#include <iostream>
#include <cstdint>
#include <limits>
#include <bitset>
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

/* Example 1: Sensor array
   - Each sensor maps to one bit in a 32-bit status register.
   - Count active sensors and decide to wake/aggregate when threshold reached.
*/
void sensorArrayDemo() {
    // Simulate 32 sensors: create a bitmask where 1 = active
    uint32_t sensors = 0;
    sensors |= (uint32_t(1) << 0);  // sensor 0 active
    sensors |= (uint32_t(1) << 3);  // sensor 3 active
    sensors |= (uint32_t(1) << 7);  // sensor 7 active
    sensors |= (uint32_t(1) << 12); // sensor 12 active

    std::cout << "Sensor bitmask: " << std::bitset<32>(sensors) << "\n";
    uint32_t active = countSetBits(sensors);
    std::cout << "Active sensors: " << active << "\n";

    const uint32_t wakeThreshold = 3;
    if (active >= wakeThreshold) {
        std::cout << "Decision: Wake MCU and aggregate sensor data\n";
    } else {
        std::cout << "Decision: Stay in low-power mode\n";
    }
    std::cout << "----\n";
}

int main() {
    sensorArrayDemo();

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