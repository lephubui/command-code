# Problem: Validate a stream of packets from multiple sensors, checking for missing packets, duplicates, and checksum errors.
# Each packet has an id, sequence number, and checksum.
# The checksum is valid if it matches the expected checksum calculated as seq XOR 0xABCD.
# Emit errors in the order they are detected: missing packets, duplicates, and bad checksums
# Only report the first missing packet when a gap appears.
# Example input:
# [{"id":"A","seq":10,"checksum":"abcd"},
#  {"id":"A","seq":12,"checksum":"abce"},  # missing 11
#  {"id":"A","seq":12,"checksum":"abce"},  # duplicate 12
#  {"id":"A","seq":11,"checksum":"xxxx"},  # bad_checksum 11 (arrives late)
#  {"id":"B","seq":5,"checksum":"abcf"},    # first packet for B
#  {"id":"B","seq":5,"checksum":"abcf"},    # duplicate 5
# ]
# Expected output:
# ["A missing 11", "A duplicate 12", "A bad_checksum 11", "B duplicate 5"]

from typing import List, Dict, Set

def validate_stream(packets: List[dict]) -> List[str]:
    """
    Emits errors in arrival order:
      "<id> missing X"
      "<id> duplicate X"
      "<id> bad_checksum X"
    Only the *first* missing number is reported when a gap appears.
    """

    def expected_checksum(seq: int) -> str:
        return hex(seq ^ 0xABCD)[2:]  # no leading '0x'

    # Per-sensor state:
    #  max_contig: highest contiguous sequence observed (None until first packet)
    #  ahead: set of out-of-order seqs > max_contig that we've seen
    state: Dict[str, Dict[str, object]] = {}
    errors: List[str] = []

    for p in packets:
        sid = p["id"]
        seq = p["seq"]
        chk = p["checksum"]

        # ensure sensor state
        if sid not in state:
            state[sid] = {"max": None, "ahead": set()}  # type: ignore
        max_contig = state[sid]["max"]  # type: ignore
        ahead: Set[int] = state[sid]["ahead"]  # type: ignore

        # 1) checksum first
        if chk != expected_checksum(seq):
            errors.append(f"{sid} bad_checksum {seq}")
            # We *still* process duplicates/missing based on policy; commonly OK to continue processing.
            # If the requirement were "discard bad packets", we'd 'continue' here.

        # 2) duplicate detection (must be independent of checksum correctness)
        is_dup = False
        if max_contig is None:
            # no duplicates possible yet unless the same seq repeats immediately
            is_dup = (seq in ahead)  # usually false at first sight
        else:
            if seq <= max_contig or seq in ahead:
                errors.append(f"{sid} duplicate {seq}")
                is_dup = True

        # 3) missing detection (report only first missing number at gap appearance)
        if max_contig is None:
            # first packet for this sensor: no missing implied
            pass
        else:
            if seq > max_contig + 1:
                # report only the first missing number
                errors.append(f"{sid} missing {max_contig + 1}")

        # 4) state update
        if max_contig is None:
            # initialize contiguous frontier
            state[sid]["max"] = seq
        else:
            if seq == max_contig + 1:
                # advance contiguous frontier and collapse any buffered out-of-order seqs
                max_contig += 1
                while (max_contig + 1) in ahead:
                    ahead.remove(max_contig + 1)
                    max_contig += 1
                state[sid]["max"] = max_contig
            elif seq > max_contig + 1:
                ahead.add(seq)
            # if seq <= max_contig or in ahead, we already flagged duplicate above

    return errors

# Example usage:
if __name__ == "__main__":

    packets = [
    {"id":"A","seq":10,"checksum":hex(10 ^ 0xABCD)[2:]},
    {"id":"A","seq":12,"checksum":hex(12 ^ 0xABCD)[2:]},  # missing 11
    {"id":"A","seq":12,"checksum":hex(12 ^ 0xABCD)[2:]},  # duplicate 12
    {"id":"A","seq":11,"checksum":"xxxx"},                # bad_checksum 11 (arrives late)
    {"id":"B","seq":5,"checksum":hex(5 ^ 0xABCD)[2:]},
    {"id":"B","seq":5,"checksum":hex(5 ^ 0xABCD)[2:]},    # duplicate 5
    ]
    # Expected (order of detection while scanning):
    # ["A missing 11", "A duplicate 12", "A bad_checksum 11", "B duplicate 5"]
    result = validate_stream(packets)
    print(result)
    
    # write to log.txt file
    with open("log.txt", "w") as f:
        for line in result:
            f.write(line + "\n")