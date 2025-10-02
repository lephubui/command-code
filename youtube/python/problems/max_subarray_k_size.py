# Problem: Given an array of integers numbers and an integer k, find the maximum sum of a subarray of size k.
# Return a tuple containing the maximum sum and the starting index of the subarray.
# Example:
# Input: numbers = [1, 4, 2, 10, 23, 3, 1, 0, 20], k = 4
# Output: (39, 3)
# Explanation: The subarray with the maximum sum is [10, 23, 3, 1] which starts at index 3 and has a sum of 39.
# Constraints: The input array must contain at least k elements.
# The function should handle edge cases, such as when all elements are negative or when k equals the length of the array.
# 10^6 >= len(numbers) >= k >= 1
# -10^6 <= numbers[i] <= 10^6
# The solution should have a time complexity of O(n) where n is the length of the input array.
# You may use built-in functions and data structures.
def maximum_sum(numbers, k):
    """ Implement the function to find maximum subarray of size k in numbers """
    n = len(numbers)
    
    if (n < k):
        return ()
    
    sum_k_elements = sum(numbers[:k])
    max_sum = sum_k_elements
    max_index = 0

    for i in range(k, n):
        new_k_elements = sum_k_elements - numbers[i - k] + numbers[i]
        if (new_k_elements > max_sum):
            max_sum = new_k_elements
            max_index = i - k + 1
        sum_k_elements = new_k_elements

    return (max_sum, max_index)

if __name__ == "__main__":
    print(maximum_sum([1, 4, 2, 10, 23, 3, 1, 0, 20], 4))  # (39, 3)
    print(maximum_sum([-1, -2, -3, -4], 2))               # (-3, 0)
    print(maximum_sum([5, 5, 5, 5], 4))                  # (20, 0)
    print(maximum_sum([1, 2, 3], 3))                      # (6, 0)
    print(maximum_sum([1], 1))                            # (1, 0)
    print(maximum_sum([1, -1, 1, -1], 2))                 # (0, 0)
    print(maximum_sum([10**6] * (10**6), 10**6))         # (1000000000000, 0)
    print(maximum_sum([1, 2], 3))                         # ()
    print(maximum_sum([0, -1, -2, -3], 2))                # (-1, 0)
    print(maximum_sum([3, -2, 5, -1], 2))                 # (3, 0)
