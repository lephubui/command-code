# Implement a binary search algorithm
# Problem: Given a sorted array of integers nums and an integer target, return the index of target if it is present in nums. If not, return -1.
# You must write an algorithm with O(log n) runtime complexity.
# Example:
# Input: nums = [-1,0,3,5,9,12], target = 9
# Output: 4
# Explanation: 9 exists in nums and its index is 4.
# Constraints:
# 1 <= nums.length <= 10^4
# -10^4 < nums[i], target < 10^4

def binary_search(nums, target):
    """Implement the binary search algorithm to find the index of target in nums."""
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1 # Target not found

if __name__ == "__main__":
    print(binary_search([-1,0,3,5,9,12], 9))  # Output: 4
    print(binary_search([-1,0,3,5,9,12], 2))  # Output: -1
    print(binary_search([1,2,3,4,5], 3))      # Output: 2
    print(binary_search([1,2,3,4,5], 6))      # Output: -1
    print(binary_search([10,20,30,40,50], 10)) # Output: 0
    print(binary_search([10,20,30,40,50], 50)) # Output: 4