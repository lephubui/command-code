# Problem Statement: You are tasked with designing a Python function called solution() that processes a series of distinct requests or operations.
# These operations consist of a list of two integers: one signifies the type of operation, and the other is the operand.

# There are three kinds of actions you will need to handle:
#
# Adding a number to the set (operation type 0). If the number is already in the set, you should ignore it.
# Removing a number from the set (operation type 1). Whenever this operation is invoked, it is guaranteed that the number exists in the set.
# Finding the maximum number in the set (operation type 2).
#
# The list of operations is delivered to your function as a 2D array, where each subarray contains two values — the type of operation and the operand. 
# The function should output an array of results for every operation. For operation types 0 and 1, the function should return the count of unique elements in the set after the operation. 
# For operation type 2, the function should return the maximum number in the set. If the set is empty, the function should return -1.
# Constraints:
# The number of operations can be as large as 10^5.
# The integers involved in the operations can range from -10^5 to 10^5.
# The operation type will always be one of the three specified (0, 1, or 2).

from sortedcontainers import SortedList

def solution(operations):
    result = []
    max_list = SortedList()

    track_val = 0
    for opr in operations:
        if opr[0] == 0:
            idx = max_list.bisect_left(opr[1])
            if idx == len(max_list) or max_list[idx] != opr[1]:
                max_list.add(opr[1])
            result.append(len(max_list))
        elif opr[0] == 1:
            max_list.discard(opr[1])
            result.append(len(max_list))
        else:
            if len(max_list) != 0:
                track_val = max_list[-1]
                result.append(track_val)
            else:
                result.append(-1)


    return result

if __name__ == "__main__":
    # Test case 1: Basic operations
    operations = [[0, 5], [0, 3], [2, 0], [1, 5], [2, 0]]
    print(solution(operations))  # Expected output: [1, 2, 5, 1, 3]

    # Test case 2: Removing all elements
    operations = [[0, 10], [0, 20], [1, 10], [1, 20], [2, 0]]
    print(solution(operations))  # Expected output: [1, 2, 1, 0, -1]

    # Test case 3: Adding duplicates
    operations = [[0, 7], [0, 7], [2, 0], [1, 7], [2, 0]]
    print(solution(operations))  # Expected output: [1, 1, 7, 0, -1]