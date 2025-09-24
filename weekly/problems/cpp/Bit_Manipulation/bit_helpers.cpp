#include <cstddef>
#include <cstdint>
#include <type_traits>
#include <bitset>
#include <iostream>

// constexpr-friendly mask generator (returns 0 if index out of range)
template<typename T>
constexpr T bit_mask(std::size_t i) noexcept {
    static_assert(std::is_unsigned<T>::value, "T must be unsigned");
    return (i < sizeof(T) * 8u) ? (T(1) << i) : T(0);
}

template<typename T>
constexpr T set_bit(T x, std::size_t i) noexcept {
    return x | bit_mask<T>(i);
}

template<typename T>
constexpr T clear_bit(T x, std::size_t i) noexcept {
    return x & ~bit_mask<T>(i);
}

template<typename T>
constexpr T toggle_bit(T x, std::size_t i) noexcept {
    return x ^ bit_mask<T>(i);
}

template<typename T>
constexpr bool test_bit(T x, std::size_t i) noexcept {
    return (x & bit_mask<T>(i)) != 0;
}

// compile-time sanity checks
static_assert(set_bit<std::uint32_t>(0u, 3u) == 0x8u, "set_bit check");
static_assert(clear_bit<std::uint32_t>(0xFu, 3u) == 0x7u, "clear_bit check");
static_assert(toggle_bit<std::uint8_t>(0x1u, 0u) == 0x0u, "toggle_bit check");
static_assert(test_bit<std::uint32_t>(0x8u, 3u) == true, "test_bit check");

int main() {
    using U32 = std::uint32_t;
    U32 x = 0;
    std::cout << "start : " << std::bitset<32>(x) << " (" << x << ")\n";

    x = set_bit<U32>(x, 3);
    std::cout << "set_bit(0,3) -> " << std::bitset<32>(x) << " (" << x << ")\n";

    x = set_bit<U32>(x, 7);
    std::cout << "set_bit(...,7) -> " << std::bitset<32>(x) << " (" << x << ")\n";

    x = clear_bit<U32>(x, 3);
    std::cout << "clear_bit(...,3) -> " << std::bitset<32>(x) << " (" << x << ")\n";

    x = toggle_bit<U32>(x, 7);
    std::cout << "toggle_bit(...,7) -> " << std::bitset<32>(x) << " (" << x << ")\n";

    std::cout << "test_bit(...,0) = " << test_bit<U32>(x, 0) 
              << ", test_bit(...,7) = " << test_bit<U32>(x, 7) << "\n";

    return 0;
}