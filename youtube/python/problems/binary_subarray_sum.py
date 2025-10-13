# Target Sum Between Two Arrays
# Given two arrays of integers arrA and arrB, find the pair of indices (i, j) such that arrA[i] + arrB[j] == 0.
# If multiple pairs exist, return the pair with the smallest i. If no such pair exists, return an empty array.
# Example:
# Input: arrA = [1, 2, 3], arrB = [-2, -1, 0]
# Output: [0, 1] (since arrA[0] + arrB[1] == 0)
# Constraints:
# - Both arrays have the same length n (1 <= n <= 10^5).
# - Each element in arrA and arrB is an integer in the range [-10^9, 10^9].
# Time Complexity: O(n)
# Space Complexity: O(n)
# Solution:
# 1. Create a hash map to store the values of arrA and their corresponding indices.
# 2. Iterate through arrB and for each element, check if its negation exists in the hash map.
# 3. If a match is found, store the pair of indices.
# 4. Return the pair with the smallest i if multiple pairs exist, otherwise return an empty array.
# 5. If no pairs are found, return an empty array.

def numSubarraysWithSum(self, nums, goal):
    """
    :type nums: List[int]
    :type goal: int
    :rtype: int
    """
    def f(nums, goal):
        if goal < 0:
            return 0
        l = 0
        sum_ = 0
        count = 0
        for r in range(len(nums)):
            sum_ += nums[r]
            
            # Shrink window if sum_ exceeds goal
            while l <= r and sum_ > goal:
                sum_ -= nums[l]
                l += 1

            count += (r - l + 1)
        return count
    
    return f(nums, goal) - f(nums, goal - 1)

if __name__ == "__main__":
    nums = [1,0,1,0,1]
    goal = 2
    print(numSubarraysWithSum(None, nums, goal))  # Output: 4
