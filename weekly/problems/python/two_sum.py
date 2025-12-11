# Find two sum problem solution
# Problem: Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
# You may assume that each input would have exactly one solution, and you may not use the same element twice.
# You can return the answer in any order.
# Example:
# Input: nums = [2,7,11,15], target = 9
# Output: [0,1]
# Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
# Constraints:
# 2 <= nums.length <= 10^4
# -10^9 <= nums[i] <= 10^9
# -10^9 <= target <= 10^9
# Only one valid answer exists.

def two_sum(nums, target):
    """ Implement the function to find two indices in nums that add up to target """
    num_to_index = {}
    
    for index, num in enumerate(nums):
        complement = target - num
        if complement in num_to_index:
            return [num_to_index[complement], index]
        num_to_index[num] = index
    
    return []  # In case there is no solution, though the problem guarantees one exists

if __name__ == "__main__":
    print(two_sum([2, 7, 11, 15], 9))  # Output: [0, 1]
    print(two_sum([3, 2, 4], 6))       # Output: [1, 2]
    print(two_sum([3, 3], 6))          # Output: [0, 1]
    print(two_sum([1, 2, 3, 4, 5], 9)) # Output: [3, 4]
    print(two_sum([-1, -2, -3, -4], -6)) # Output: [1, 3]