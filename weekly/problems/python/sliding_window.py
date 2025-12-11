# Find the longest substring without repeating characters
# Problem: Given a string s, find the length of the longest substring without repeating characters.
# Example:
# Input: s = "abcabcbb"
# Output: 3
# Explanation: The answer is "abc", with the length of 3.
# Constraints:
# 0 <= s.length <= 5 * 10^4
# s consists of English letters, digits, symbols and spaces.

def length_of_longest_substring(s):
    """Implement the sliding window algorithm to find the length of the longest substring without repeating characters."""
    char_index_map = {}
    left = 0
    max_length = 0

    for right in range(len(s)):
        if s[right] in char_index_map and char_index_map[s[right]] >= left:
            left = char_index_map[s[right]] + 1
        char_index_map[s[right]] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length

if __name__ == "__main__":
    print(length_of_longest_substring("abcabcbb"))  # Output: 3
    print(length_of_longest_substring("bbbbb"))     # Output: 1
    print(length_of_longest_substring("pwwkew"))    # Output: 3
    print(length_of_longest_substring(""))           # Output: 0
    print(length_of_longest_substring("au"))        # Output: 2
    print(length_of_longest_substring("dvdf"))      # Output: 3