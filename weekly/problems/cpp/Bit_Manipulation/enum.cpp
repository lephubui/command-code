#include <cstdint>
#include <type_traits>

// quick underlying conversion
template<typename E>
constexpr auto to_underlying(E e) noexcept {
    return static_cast<std::underlying_type_t<E>>(e);
}

// bitwise operators for enum class flags
template<typename E>
constexpr E operator|(E a, E b) noexcept {
    return static_cast<E>(to_underlying(a) | to_underlying(b));
}
template<typename E>
constexpr E operator&(E a, E b) noexcept {
    return static_cast<E>(to_underlying(a) & to_underlying(b));
}
template<typename E>
constexpr E operator^(E a, E b) noexcept {
    return static_cast<E>(to_underlying(a) ^ to_underlying(b));
}
template<typename E>
constexpr E operator~(E a) noexcept {
    return static_cast<E>(~to_underlying(a));
}
template<typename E>
constexpr E& operator|=(E& a, E b) noexcept { return (a = a | b); }
template<typename E>
constexpr E& operator&=(E& a, E b) noexcept { return (a = a & b); }
template<typename E>
constexpr E& operator^=(E& a, E b) noexcept { return (a = a ^ b); }

// helpers
template<typename E>
constexpr bool has_flag(E value, E flag) noexcept {
    return (to_underlying(value) & to_underlying(flag)) != 0;
}
template<typename E>
constexpr E set_flag(E value, E flag) noexcept { return value | flag; }
template<typename E>
constexpr E clear_flag(E value, E flag) noexcept { return value & ~flag; }

// Usage example: UART control bits as enum class
enum class UARTFlags : uint32_t {
    NONE       = 0u,
    TX_ENABLE  = 1u << 0,
    RX_ENABLE  = 1u << 1,
    PARITY_EN  = 1u << 2,
    STOP_2BITS = 1u << 3,
};

// Example: prepare flags and write to a register (MMIO)
inline void write_uart_ctrl(volatile uint32_t* reg, UARTFlags flags) {
    *reg = to_underlying(flags); // safe explicit conversion
}

/* Example usage:
volatile uint32_t* UART_CTRL = reinterpret_cast<volatile uint32_t*>(0x40001000);
UARTFlags cfg = UARTFlags::TX_ENABLE | UARTFlags::RX_ENABLE;
cfg |= UARTFlags::PARITY_EN;
if (has_flag(cfg, UARTFlags::RX_ENABLE)) { ... }
cfg = clear_flag(cfg, UARTFlags::PARITY_EN);
write_uart_ctrl(UART_CTRL, cfg);
*/