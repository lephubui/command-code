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
def search_specific_words(file_path, search_words, log_level=None):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readline()
            word_counts = Counter()
            # Extract words from theline
            for line in lines:
                # Check if line matches the specific log level (when user provided)
                if log_level and not line.lower().startwith(f"{log_level.lower()} "):
                    continue
                # Extract words from line
                line_text = line.lower() 
                words = re.findall(r'\b\w+\b', line_text)
                word_counts.update(words)
            # Return counts for specified words
            # Iterate through search words list
            result = [(word, word_counts.get(word, 0)) for word in search_words]
            return result
    except (FileNotFoundError, PermissionError) as err:
        print(f"Yo, we got an error: {err}")
        return None

def process_log(file_path, level_log):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
             lines = file.readlines()
             # Store timstamp and level log
             log_entries = []
             for line in lines:
                 # Extract timestamp and log level using regex
                 match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s+(\w+)', line)
                 if match:
                     timestamp = match.group(1)
                     level = match.group(2).upper()
                     # Check only if level matches the specified log level
                     if level.lower() == level_log.lower():
                         log_entries.append((timestamp, level))
        return log_entries
    except (FileNotFoundError, PermissionError) as err:
        print(f"Yo, we got an error: {err}")
        return None

# Driver code
if __name__ == "__main__":
    # Passing the file path in the terminal when exucting the program/script
    if len(sys.argv) < 2:
        print("Usage: python3 word_counter.py <file_path> [top_n | --search word1 word2 ... | --level_log LEVEL]")
        sys.exit(1)
    
    # Get the file path
    file_path = sys.argv[1]

    if (len(sys.argv) >= 3 and sys.argv[2] == '--level_log'):
        # Edge case
        if len(sys.argv) != 4:
            print("Yo, you need to provide a single log level after --level_log (e.g: --level_log ERROR")
        log_level = sys.argv[3]
        
        # Extract time stamp
        # Define a helper funtion to get log out for level log
        log_entries = process_log(file_path, log_level)
        if log_entries is not None:
            print(f"Log Entries for {log_level.upper()} (Timestamp, Log Level):")
            if log_entries:
                for timestamp, level in log_entries:
                    print(f"{timestamp} : {level}")
            else:
                print(f"Yo, no log level found for {log_level.upper()}")

    elif (len(sys.argv) >= 3 and sys.argv[2] == '--search'):
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
