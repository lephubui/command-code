# Word Counter Implementation and Application

A Python script CLI word_counters.py
 - Count word frequencies in a text file
 - Search specific words in a text file
 - Extract specific info in a text file

## System Requirements

- **Operating System**: Ubuntu 24.04 (tested and optimized)
- **Python Version**: 3.7+
- **Dependencies**: No external dependencies for core functionality

## Overview

This project demonstrates a robust word counting algorithm that can process text files, strings, and various input formats while maintaining accuracy and performance.

## How to run
 - python3 word_counter.py <file_path> [top_n | --search word1 word2 ...| --level_log LEVEL<e.g: ERROR, DEBUG...>]
 - python3 test_word_counter.py

## Youtube playlist
 - [Python Code](https://www.youtube.com/watch?v=mnyV68QtmWM&list=PLZdyjUgq8p7k8BV9JMxfNyR3g7BVGioAl)


## Features

- **Multiple Input Sources**: Process text from files, strings, or stdin
- **Case Sensitivity Options**: Count words with or without case sensitivity
- **Special Character Handling**: Properly handles punctuation and special characters
- **Unicode Support**: Works with international characters and symbols
- **Performance Optimized**: Efficient processing for large text files

## Implementation Details

### Core Word Counter Class

```python
class WordCounter:
    def __init__(self, case_sensitive=False):
        self.case_sensitive = case_sensitive
        self.word_count = {}
    
    def count_words(self, text):
        # Implementation handles tokenization and counting
        pass
    
    def count_from_file(self, filepath):
        # File processing implementation
        pass
```

### Key Methods

- `count_words(text)`: Count words in a given string
- `count_from_file(filepath)`: Process text files
- `get_most_common(n)`: Return top N most frequent words
- `get_total_words()`: Return total word count
- `reset()`: Clear current word counts

## Usage Examples

### Basic Usage

```python
from word_counter import WordCounter

# Initialize counter
counter = WordCounter(case_sensitive=False)

# Count words in text
text = "Hello world! This is a test. Hello again."
result = counter.count_words(text)
print(result)  # {'hello': 2, 'world': 1, 'this': 1, 'is': 1, 'a': 1, 'test': 1, 'again': 1}

# Count from file
counter.count_from_file('sample.txt')
```

### Advanced Features

```python
# Case sensitive counting
case_counter = WordCounter(case_sensitive=True)

# Get most common words
top_words = counter.get_most_common(5)

# Total word count
total = counter.get_total_words()
```

## Unit Testing

### Test Structure

The unit tests cover all major functionality using Python's `unittest` framework:

```python
import unittest
from word_counter import WordCounter

class TestWordCounter(unittest.TestCase):
    def setUp(self):
        self.counter = WordCounter()
    
    def test_basic_counting(self):
        # Test basic word counting functionality
        pass
    
    def test_case_sensitivity(self):
        # Test case sensitive vs insensitive counting
        pass
    
    def test_file_processing(self):
        # Test file input processing
        pass
```

### Test Categories

1. **Basic Functionality Tests**
   - Simple word counting
   - Empty string handling
   - Single word processing

2. **Edge Case Tests**
   - Special characters and punctuation
   - Numbers and mixed content
   - Unicode and international characters

3. **File Processing Tests**
   - Valid file processing
   - File not found handling
   - Large file performance

4. **Configuration Tests**
   - Case sensitivity options
   - Reset functionality
   - State management

### Running Tests

```bash
# Run all tests
python -m unittest test_word_counter.py

# Run specific test class
python -m unittest test_word_counter.TestWordCounter

# Run with verbose output
python -m unittest -v test_word_counter.py
```

## Requirements

- **Platform**: Ubuntu 24.04 LTS
- Python 3.7+
- No external dependencies for core functionality
- `unittest` (built-in) for testing

## Performance Considerations

- Memory efficient for large files using generators
- O(n) time complexity for word counting
- Optimized regex patterns for tokenization
- Lazy loading for file processing

## Error Handling

The implementation includes robust error handling for:
- Invalid file paths
- Encoding issues
- Memory constraints
- Invalid input types

## Contributing

When contributing to this project:
1. Maintain test coverage above 95%
2. Follow PEP 8 style guidelines
3. Add unit tests for new features
4. Update documentation for API changes

