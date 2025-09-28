# Problem
# You are given a string s. We want to partition the string into as many parts as
# possible so that each letter appears in at most one part. Return a list of integers
# representing the size of these parts.
# function must perfectly divide the string, 
# ensuring a unique occurrence of each character per partition, while efficiently reporting the length of these partitions.

# Constraints:
# The length of the input string n will be in the range of 1 ≤ n ≤ 1000000.
# All characters in the string will be lower-case English alphabets ('a' to 'z').
# The time complexity of the solution should be 
# O(n) and the space complexity should be O(n).

def string_partition(s):
    # Using hash map
    last_occurrence = {}
    result = []
    for i, chr in enumerate(s):
        last_occurrence[chr] = i
    
    start = 0
    end = 0
    for i, chr in enumerate(s):
        end = max(end, last_occurrence[chr])
        if i == end:
            result.append(i - start + 1)
            start = i + 1

    return result