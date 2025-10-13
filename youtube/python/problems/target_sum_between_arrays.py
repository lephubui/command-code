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
# Key Insight:
# Suppose you want to find i and j such that:
#   arrA[i]+arrA[j]=arrB[i]+arrB[j]
# If you rearrange, you get:
#   arrA[i]−arrB[i] = −(arrA[j]−arrB[j])
# So, if you know the difference at one index, you can look for its negative at another index!

def solution(arrA, arrB):
    arr_map = {}
    pair_list = []
    for i in range(len(arrA)):
        compute = arrA[i] - arrB[i]
        if -compute in arr_map:
            pair_list.append([arr_map[-compute], i])
        if compute not in arr_map:
            arr_map[compute] = i
    
    if pair_list:
        return min(pair_list)

    return []

# Driver code
if __name__ == "__main__":
    arrA = [1, 2, 3]
    arrB = [-2, -1, 0]
    print(solution(arrA, arrB))  # Output: [0, 1]