# Problem: Given an array of integers, count the number of triplets (i, j, k) such that arr[i] == arr[j] and i < j < k.
# Example: For the array [1, 2, 3, 1, 1, 3], the triplets are (0,3,4) for the number 1. Thus, the output should be 3.
# Constraints: The array length can be up to 10^5, and the integers can range from -10^9 to 10^9.
# Solution: Use a frequency map to count occurrences of each number, then calculate the number of triplets using combinatorial counting.
# Time Complexity: O(n)
# Space Complexity: O(n)

from collections import Counter

def solution(s):
    map_s = Counter(s)
    counter = 0
    sum_map =sum(map_s.values())
    for k in map_s:
        n = map_s[k]
        compute_pairs = n*(n-1) // 2
        counter += compute_pairs*(sum_map - map_s[k])

    return counter

if __name__ == "__main__":
    # Test case 1: Original example
    s = [1, 2, 3, 1, 1, 3]
    result = solution(s)
    print(f"Test 1 - s: {s}")
    print(f"Output: {result}")  # Expected: 8
    print()
    
    # Test case 2: No pairs
    s = [1, 2, 3, 4]
    result = solution(s)
    print(f"Test 2 - s: {s}")
    print(f"Output: {result}")  # Expected: 0
    print()
    
    # Test case 3: All elements the same
    s = [5, 5, 5, 5]
    result = solution(s)
    print(f"Test 3 - s: {s}")
    print(f"Output: {result}")  # Expected: 12
    print()
    
    # Test case 4: Mixed values
    s = [1, 2, 2, 3, 3, 3]
    result = solution(s)
    print(f"Test 4 - s: {s}")
    print(f"Output: {result}")  # Expected: 16
    print()
    
    # Test case 5: Negative and positive values
    s = [-1, -1, 0, 0, 0, 1]
    result = solution(s)
    print(f"Test 5 - s: {s}")
    print(f"Output: {result}")  # Expected: 14
    print()