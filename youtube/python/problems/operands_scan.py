# Program to process a list of operations involving adding numbers,
# retrieving the maximum number, and removing the maximum number.
# Uses a max-heap to efficiently manage the numbers.
# Operations are given as pairs where the first element is the operation
# type ('Add', 'Max', 'RemoveMax') and the second element is the number
# to be added (only for 'Add' operations).
# Example input: [('Add', 3), ('Add', 5), ('Max',), ('RemoveMax',), ('Max',)]
# Example output: [5, 3]

import heapq

def solution(operations):
    max_output = []
    nums = []
    for pair in operations:
        if pair[0] == 'Add':
            heapq.heappush(nums, -pair[1])
        elif pair[0] == 'Max' and nums:
            max_output.append(-nums[0])
        else:
            heapq.heappop(nums)
    
    return max_output

if __name__ == "__main__":
    operations = [('Add', 3), ('Add', 5), ('Max',), ('RemoveMax',), ('Max',)]
    print(solution(operations))  # Output: [5, 3]