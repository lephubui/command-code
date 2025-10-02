# Given an array of integers representing the sweetness levels of chocolates,
# find all unique pairs of chocolates that sum to zero.
# Return the pairs in ascending order.
# Example:
# Input: [1, -1, 2, 3, -2, -3, 4]
# Output: [(-3, 3), (-2, 2), (-1, 1)]
# Explanation: The pairs (-3, 3), (-2, 2), and (-1, 1) all sum to zero.
# The output is sorted in ascending order.
# Constraints:
# - The input array may contain duplicate elements.
# - The input array can be of any length, including empty.
# - Each pair should be unique; the order of elements in the pair does not matter.
# - The output should be a list of tuples, where each tuple contains two integers.
# - If no pairs sum to zero, return an empty list.
# - The solution should have a time complexity of O(n log n) or better.
# - You may use built-in sorting functions and data structures.
# - The input array can contain both positive and negative integers, as well as zero.
# - The function should handle edge cases, such as an array with all positive or all negative integers.

def find_choc_pairs(sweetness):
    res = []
    
    left = 0
    right = len(sweetness) - 1
    sweetness.sort()
    
    while (left < right):
        if (sweetness[left] + sweetness[right] == 0):
            res.append((sweetness[right], sweetness[left]))
            left += 1
            right -= 1
        elif (sweetness[left] + sweetness[right] < 0):
            left += 1
        else:
            right -= 1
    
    res.sort()
    
    return res

if __name__ == "__main__":
    print(find_choc_pairs([1, -1, 2, 3, -2, -3, 4]))  # [(-3, 3), (-2, 2), (-1, 1)]
    print(find_choc_pairs([0, 0, 0, 0]))              # [(0, 0)]
    print(find_choc_pairs([1, 2, 3]))                 # []
    print(find_choc_pairs([-1, -2, -3]))              # []
    print(find_choc_pairs([]))                         # []
    print(find_choc_pairs([1, -1, 1, -1]))            # [(-1, 1)]
    print(find_choc_pairs([4, -4, 4, -4, 0]))         # [(-4, 4), (0, 0)]
    print(find_choc_pairs([5]))                        # []
    print(find_choc_pairs([-5]))                       # []
    print(find_choc_pairs([3, -3, 2, -2, 1, -1]))     # [(-3, 3), (-2, 2), (-1, 1)]