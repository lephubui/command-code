# Problem: Find the longest contiguous subarray with sum exactly k
# Assumption: input array contains positive integers only (sliding-window valid)
# Return the longest subarray. If multiple such subarrays exist, return any one of them.
# Example:
# Input: array = [1, 2, 3], k = 6
# Output: [1, 2, 3]
# Constraints: Array elements are positive integers.
# The length of the input array n will be in the range of 1 ≤ n ≤ 1000000.
# The elements of the array will be in the range of 1 to 10^6.
# The solution should have a time complexity of O(n) where n is the length of the input array.

def get_longest_subarray(array, k):
    # Initialize pointers and tracking variables
    left = 0
    right = 0
    curr_sum = 0
    max_size = 0
    best_left = 0
    best_right = 0

    # Use a sliding window approach (valid because array contains only positive numbers)
    while right < len(array):
        # Expand window to the right while curr_sum < k
        if curr_sum < k:
            curr_sum += array[right]
            right += 1
        # If current sum matches k, update best window if larger
        elif curr_sum == k:
            current_size = right - left
            if current_size > max_size:
                best_left = left
                best_right = right
                max_size = current_size
            # Move left pointer to continue searching
            curr_sum -= array[left]
            left += 1
        # If current sum exceeds k, shrink window from the left
        else:
            curr_sum -= array[left]
            left += 1

    # Final check in case the last window matches k and is the largest
    if curr_sum == k and (right - left) > max_size:
        best_left = left
        best_right = right

    # Return the longest subarray found (may be empty)
    return array[best_left:best_right]


if __name__ == "__main__":
    # Positive-only test cases
    print(get_longest_subarray([1, 2, 3], 6))               # [1, 2, 3]
    print(get_longest_subarray([1, 1, 1, 1, 1], 3))         # [1, 1, 1] (earliest longest)
    print(get_longest_subarray([5, 1, 2, 3, 5], 8))         # [5, 1, 2]
    print(get_longest_subarray([10**6] * 10, 10**6))        # [1000000]
    print(get_longest_subarray([1], 1))                     # [1]
    print(get_longest_subarray([1, 2, 3], 7))               # [] (no match)
    print(get_longest_subarray([2, 2, 2, 2], 4))            # [2,2] (earliest)
