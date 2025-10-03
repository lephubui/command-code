# Problem: Longest contiguous subarray with sum exactly k (handles negatives)
#
# Description:
#   Given an integer array (may contain negative numbers) and an integer k,
#   return the longest contiguous subarray whose elements sum to exactly k.
#   If multiple subarrays have the same maximum length, return the earliest one
#   (smallest start index). Return an empty list if no such subarray exists.
#
# Approach:
#   Use prefix-sums and a map that records the first index each prefix sum appears.
#   For current prefix sum `s` at index i, if (s - k) has appeared before at index j,
#   then subarray (j+1..i) sums to k. By recording only the first occurrence of
#   each prefix sum we ensure we get the longest (and earliest) candidate for any i.
#
# Complexity:
#   Time: O(n) — single pass, map lookups are average O(1)
#   Space: O(n) — for prefix-sum map
#
# Notes:
#   - Works with negative numbers and zeros.
#   - For very large inputs, ensure Python recursion/limits or memory are sufficient.
#
# Examples:
#   get_longest_subarray([1, -1, 5, -2, 3], 3) -> [1, -1, 5, -2]  (longest, earliest)
#   get_longest_subarray([1, 2, 3], 6) -> [1, 2, 3]
#   get_longest_subarray([0, 0, 0], 0) -> [0, 0, 0]

def get_longest_subarray(array, k):
    """
    Return the longest contiguous subarray whose sum is exactly k.
    If multiple longest subarrays exist, return the earliest one (smallest start index).
    Returns [] if no such subarray exists.
    """
    first_idx = {0: -1}              # prefix sum -> first index where it appears
    s = 0
    best_len = 0
    best_l = 0
    best_r = -1

    for i, v in enumerate(array):
        s += v
        # record first occurrence of this prefix sum
        if s not in first_idx:
            first_idx[s] = i

        need = s - k
        if need in first_idx:
            start = first_idx[need] + 1
            length = i - first_idx[need]
            # update when longer, or same length but earlier start
            if length > best_len or (length == best_len and start < best_l):
                best_len = length
                best_l = start
                best_r = i

    if best_r >= 0:
        return array[best_l:best_r + 1]
    return []

if __name__ == "__main__":
    print(get_longest_subarray([1, -1, 5, -2, 3], 3))  # [1, -1, 5, -2]
    print(get_longest_subarray([3, 1, -4, 2, -1, 6], 5))  # [1, -4, 2, -1, 6]
    print(get_longest_subarray([1, 2, 3], 6))  # [1, 2, 3]
    print(get_longest_subarray([-1, -1, -1], -2))  # [-1, -1]
    print(get_longest_subarray([1, 2, 3], 7))  # []
    print(get_longest_subarray([10**6] * (10**6), 10**6)[:3])  # show prefix of large result
    print(get_longest_subarray([1], 1))  # [1]
    print(get_longest_subarray([1], 0))  # []
    print(get_longest_subarray([0, 0, 0], 0))  # [0, 0, 0]