import re
import sys
from collections import Counter

def count_words(file_path, top_n_input=''):
    try:
        top_n = int(top_n_input) if top_n_input else 5
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read().lower()
            words = re.findall(r'\b\w+\b', text)
            word_counts = Counter(words)
            top_words = word_counts.most_common(top_n)
            return top_words
    except ValueError:
        print(f"Yo, we need an iteger for top words")
        sys.exit(1)
    except (FileNotFoundError, PermissionError) as err:
        print(f"Yo, we got an error: {err}")
        return None

# search specific words 
def search_specific_words(file_path, search_words):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read().lower()
            # remove the puntuation
            words = re.findall(r'\b\w+\b', text)
            word_counts = Counter(words)
            # Iterate through search words list
            result = [(word, word_counts.get(word, 0)) for word in search_words]
            return result
    except (FileNotFoundError, PermissionError) as err:
        print(f"Yo, we got an error: {err}")
        return None

# Driver code
if __name__ == "__main__":
    # Passing the file path in the terminal when exucting the program/script
    if len(sys.argv) < 2:
        print("Usage: python3 word_count.py <file_path> [top_n | --search word1 word2 ...]")
        sys.exit(1)
    
    # Check if search mode is requested
    file_path = sys.argv[1]
    if (len(sys.argv) >= 3 and sys.argv[2] == '--search'):
        search_words = sys.argv[3:] # Get all words after --search
        if not search_words:
            print("Please provide words to search for --search mode")
        result = search_specific_words(file_path, search_words)
        # Check if result is empty or not
        if result is not None:
            for word, count in result:
                print(f"{word} : {count}")
    else:
        # Original top_n words funtionality
        top_n = int(sys.argv[2]) if len(sys.argv) == 3 else 5

        result = count_words(file_path, top_n)
        if result is not None:
           for word, count in result:
               print(f"{word} : {count}")
