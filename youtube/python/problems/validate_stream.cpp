// Problem: Validate a stream of packets from multiple sensors, checking for missing packets,
// duplicates, and checksum errors. Each packet has an id, sequence number, and checksum.
// Checksum is valid if it matches expected checksum calculated as seq XOR 0xABCD.
// Emit errors in the order they are detected while scanning:
//   - missing: only report the first missing number when a gap appears
//   - duplicate: repeated seq for a sensor
//   - bad_checksum: checksum mismatch
//
// Example input:
// [
//   {"id":"A","seq":10,"checksum":"abcd"},
//   {"id":"A","seq":12,"checksum":"abce"},  // missing 11
//   {"id":"A","seq":12,"checksum":"abce"},  // duplicate 12
//   {"id":"A","seq":11,"checksum":"xxxx"},  // bad_checksum 11 (arrives late)
//   {"id":"B","seq":5,"checksum":"abcf"},   // first packet for B
//   {"id":"B","seq":5,"checksum":"abcf"},   // duplicate 5
// ]
// Expected output:
// ["A missing 11", "A duplicate 12", "A bad_checksum 11", "B duplicate 5"]

#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <string>
#include <sstream>
#include <iostream>
#include <fstream>

struct Packet {
    std::string id;
    int seq{};
    std::string checksum; // lowercase hex string without 0x
};

static std::string expected_checksum(int seq) {
    unsigned val = static_cast<unsigned>(seq) ^ 0xABCDu;
    std::ostringstream oss;
    oss << std::hex << std::nouppercase << val; // default is lowercase
    return oss.str();
}

struct SensorState {
    bool has_max = false;
    int max_contig = 0; // valid only if has_max
    std::unordered_set<int> ahead; // out-of-order seqs > max_contig
    // To ensure we report only the first missing when a gap appears
    bool missing_reported = false;
    int last_missing_value = 0; // valid only if missing_reported
};

std::vector<std::string> validate_stream(const std::vector<Packet>& packets) {
    std::unordered_map<std::string, SensorState> state;
    std::vector<std::string> errors;

    for (const auto& p : packets) {
        auto& st = state[p.id];

        // 1) checksum first
        if (p.checksum != expected_checksum(p.seq)) {
            errors.emplace_back(p.id + " bad_checksum " + std::to_string(p.seq));
        }

        // 2) duplicate detection (independent of checksum correctness)
        bool is_dup = false;
        if (!st.has_max) {
            // no duplicates possible yet unless we've seen same out-of-order seq
            is_dup = (st.ahead.find(p.seq) != st.ahead.end());
            if (is_dup) {
                errors.emplace_back(p.id + " duplicate " + std::to_string(p.seq));
            }
        } else {
            if (p.seq <= st.max_contig || st.ahead.find(p.seq) != st.ahead.end()) {
                errors.emplace_back(p.id + " duplicate " + std::to_string(p.seq));
                is_dup = true;
            }
        }

        // 3) missing detection (report only first missing number when a gap appears)
        if (st.has_max) {
            if (p.seq > st.max_contig + 1) {
                int missing_first = st.max_contig + 1;
                // Only report once per gap; if we already reported this missing value, skip
                if (!st.missing_reported || st.last_missing_value != missing_first) {
                    errors.emplace_back(p.id + " missing " + std::to_string(missing_first));
                    st.missing_reported = true;
                    st.last_missing_value = missing_first;
                }
            }
        }

        // 4) state update
        if (!st.has_max) {
            st.has_max = true;
            st.max_contig = p.seq;
            // gap closed or not relevant on first packet
            st.missing_reported = false;
        } else {
            if (p.seq == st.max_contig + 1) {
                // advance contiguous frontier and collapse any buffered out-of-order seqs
                st.max_contig += 1;
                while (st.ahead.find(st.max_contig + 1) != st.ahead.end()) {
                    st.ahead.erase(st.max_contig + 1);
                    st.max_contig += 1;
                }
                // once max advances, any prior gap is considered closed
                st.missing_reported = false;
            } else if (p.seq > st.max_contig + 1) {
                st.ahead.insert(p.seq);
            }
            // if seq <= max_contig or in ahead, duplicate already flagged above
        }
    }

    return errors;
}

#ifdef VALIDATE_STREAM_MAIN
int main() {
    std::vector<Packet> packets = {
        {"A", 10, expected_checksum(10)},
        {"A", 12, expected_checksum(12)}, // missing 11
        {"A", 12, expected_checksum(12)}, // duplicate 12
        {"A", 11, "xxxx"},               // bad_checksum 11 (arrives late)
        {"B", 5, expected_checksum(5)},
        {"B", 5, expected_checksum(5)},  // duplicate 5
    };

    auto result = validate_stream(packets);
    for (const auto& s : result) {
        std::cout << s << "\n";
    }

    std::ofstream ofs("log.txt");
    for (const auto& s : result) {
        ofs << s << '\n';
    }
    return 0;
}
#endif
