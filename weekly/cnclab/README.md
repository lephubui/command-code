
# CNC Lab: Beginner Network Security Labs

## Disclaimer

These labs are intended for educational purposes only. All activities and simulations are designed to be performed in a controlled environment. Do not use any techniques or tools learned here to attack, disrupt, or compromise any real-world systems or networks without proper authorization. The authors and maintainers are not responsible for any misuse of the information provided.

# CNC Lab: Beginner Network Security Labs

This project contains interactive labs designed for beginner students to study and practice network security concepts. The labs are organized into two levels:

## Level 1: Fundamentals

Labs in this level introduce basic concepts and tools in network security. Topics include:

- Understanding IP addressing and subnets
- Using basic network utilities (ping, traceroute, nslookup)
- Introduction to firewalls and simple packet filtering
- Exploring common network protocols (TCP, UDP, ICMP)

## Level 2: Applied Security

Labs in this level build on the fundamentals and introduce hands-on security scenarios. Topics include:

- Simulating network attacks (e.g., ARP spoofing, simple DoS)
- Analyzing network traffic with Wireshark
- Setting up and testing firewall rules
- Basic intrusion detection concepts

Each lab provides guided instructions and interactive simulations to help students learn by doing. The labs are built using React and Vite for a modern, responsive experience.

---

## Development

This project uses React + Vite. For development setup and ESLint configuration, see below:

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

### Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
