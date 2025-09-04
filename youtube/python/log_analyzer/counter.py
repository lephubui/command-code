from parser import LogParser
from collections import Counter

class WordCounter:
    def __init__(self, lines):
        self.lines = lines

    def count_top_words(self, top_n):
        """Count top N most common words in the entire text file."""
        text = ' '.join(self.lines).lower()
        words = LogParser.extract_words(text)
        word_counts = Counter(words)
        return word_counts.most_common(top_n)

    def search_specific_words(self, search_words, log_level=None):
        """Search and count specific words, optionally filtered by log level."""
        word_counts = Counter()
        
        for line in self.lines:
            entry = LogParser.parse_log_entry(line)
            if log_level and (not entry or entry.loglevel.lower() != log_level.lower()):
                continue
            
            words = LogParser.extract_words(line)
            word_counts.update(words)
        
        # Return counts for the requested search words
        return [(word.lower(), word_counts.get(word.lower(), 0)) for word in search_words]

