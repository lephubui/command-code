# Problem:
#   Given a string s and integer K, return the length of the longest substring
#   that contains at most K distinct characters.
#
# Description:
#   - Input: s (str), K (int >= 0)
#   - Output: length (int) of longest substring with <= K distinct characters
#   - Example: s="eceba", K=2 -> 3 ("ece")
#   - Complexity: O(n) time, O(min(n, alphabet)) space using a sliding window + frequency map
#
# Approach:
#   Use two pointers (left x, right y). Expand right adding characters to a counter.
#   While number of distinct characters > K shrink from left until distinct count <= K.
#   Track the maximum window length seen.

def solution(s, K):
    """
    Return length of longest substring of s with at most K distinct characters.
    """
    if K == 0 or not s:
        return 0

    x = 0
    max_length = 0
    counter = {}
    for y, char in enumerate(s):
        counter[char] = counter.get(char, 0) + 1

        # Shrink window until we have at most K distinct characters
        while len(counter) > K:
            left_char = s[x]
            counter[left_char] -= 1
            if counter[left_char] == 0:
                del counter[left_char]
            x += 1

        # Window [x..y] has at most K distinct chars
        max_length = max(max_length, y - x + 1)

    return max_length


if __name__ == "__main__":
    # Basic tests / demonstration
    tests = [
        ("eceba", 2, 3),    # "ece"
        ("aa", 1, 2),       # "aa"
        ("a", 0, 0),        # K=0 -> 0
        ("", 2, 0),         # empty string -> 0
        ("abaccc", 2, 4),   # "accc"
        ("abc", 5, 3),      # K >= distinct -> whole string
    ]

    for s, k, expected in tests:
        result = solution(s, k)
        print(f"solution({s!r}, {k}) = {result}  expected={expected}")
        assert result == expected, f"fail for {s!r}, K={k}: got {result}, want {expected}"

    print("All tests passed.")
