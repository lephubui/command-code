# Problem: Given a list of words, return a dictionary with the minimum distance between each word's occurrences.
# For example, for the input ["hello", "world", "hello", "code", "world", "hello"], the output should be {'hello': 2, 'world': 3}.
# The distance is defined as the number of words between two occurrences of the same word.
# Example:
# Input: ["hello", "world", "hello", "code", "world", "hello"]
# Output: {'hello': 2, 'world': 3}
# Explanation:
# The minimum distance between the first and second occurrence of "hello" is 2 (words
# "world" and "code" are in between).
# The minimum distance between the first and second occurrence of "world" is 3 (words
# "hello", "code", and "hello" are in between).
# Constraints:
# The input list will contain only lowercase English letters.
# The length of the input list will be in the range of 1 ≤ n ≤ 100000.
# The time complexity of the solution should be O(n) and the space complexity should be O(n).
# The solution should handle cases where a word appears only once by not including it in the output dictionary.
# If a word appears multiple times, the output should include the minimum distance between any two occurrences of that word.
# If there are multiple pairs of occurrences with the same minimum distance, it should still return that minimum distance.
# The solution should be case-sensitive, treating "Word" and "word" as different words.
# The solution should be able to handle large input sizes efficiently.
# The solution should not use any external libraries or packages.

# /usr/bin/env python3
def min_word_distance(word_list):
    # map to keep track of word occurrences and distances
    map_occurrence = {}
    map_distance = {}
    
    # Iterate through the list of words
    for idx, word in enumerate(word_list):
        if word in map_occurrence:
            distance = idx - map_occurrence[word]
            if word in map_distance: # If word already in map_distance, update the minimum distance
                map_distance[word] = min(distance, map_distance[word])
            else:
                map_distance[word] = distance
        map_occurrence[word] = idx # Update the last occurrence index

    return map_distance

if __name__ == "__main__":
    word_list = ["hello", "world", "hello", "code", "world", "hello"]
    print(min_word_distance(word_list))  # Output: {'hello': 2, 'world': 3}