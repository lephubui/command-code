# Given a string s, find the character that appears in the most number of unique words.
# A word is defined as a sequence of characters separated by spaces.
# If there is a tie, return the character that appears first in the string.
# Return a tuple containing the character and the number of unique words it appears in.
# Example:
# Input: s = "apple banana apricot"
# Output: ('a', 3)
# Explanation: The character 'a' appears in "apple", "banana", and "apricot", which is 3 unique words.
# The character 'p' appears in "apple" and "apricot", which is 2 unique words.
# The character 'b' appears in "banana", which is 1 unique word.
# Constraints:
# The input string s will contain only lowercase English letters and spaces.
# The length of the input string will be in the range of 1 ≤ n ≤ 1000000.
# The time complexity of the solution should be O(n) and the space complexity should be O(n).

def find_character_with_most_unique_words(s):
    map_word = {}
    list_str = s.split()
    set_words = set()
    
    # Find all the unique words
    for word in list_str:
        if len(word) != 0:
            if word not in set_words:
                set_words.add(word)
                
    # Find all the unique characters and store them in a map
    for word in set_words:
        if len(word) != 0:
            for ch in set(word):
                if ch not in map_word:
                    map_word[ch] = 1
                else:
                    map_word[ch] += 1
    
    # Find the most count word in 
    highest_count = max(map_word.values())
    # Get key from values
    key_highest = [key for key, value in map_word.items() if value == highest_count]
    ch_check = ''
    
    # In case ther are tie for broken characters
    for char in s:
        if char in key_highest:
            ch_check = char
            break
    
    return (ch_check, highest_count)

# Driver code
if __name__ == "__main__":
    s = "apple banana apricot"
    print(find_character_with_most_unique_words(s))  # Output: ('a', 3)