# Log Analyzer

A Python-based log analysis tool that provides word counting, log level filtering, and specific word searching capabilities for text and log files.

## Overview

This project demonstrates a robust log analysis system that can process text files and log files with various filtering and analysis options. It's designed to help analyze log data, count word frequencies, and extract specific information from structured log entries.

## Features

- **Word Frequency Analysis**: Count the most common words in any text file
- **Log Level Filtering**: Extract log entries by specific log levels (ERROR, DEBUG, INFO, etc.)
- **Specific Word Search**: Search for specific words and get their occurrence counts
- **Timestamp Extraction**: Parse and display timestamps for filtered log entries
- **Flexible Input**: Support for various text formats and log file structures
- **Modular Architecture**: Separated concerns with dedicated modules for counting and processing

## System Requirements

- **Operating System**: Ubuntu 24.04 (tested and optimized)
- **Python Version**: 3.7+
- **Dependencies**: No external dependencies for core functionality

## Project Structure

```
log_analyzer/
├── main.py           # Main application with CLI interface
├── cli.py            # CLI handler for argument parsing and output formatting
├── parser.py         # Log parsing utilities and data structures
├── counter.py        # Word counting and frequency analysis module
├── processor.py      # Log processing and filtering module
├── logs.text         # Sample log file for testing
├── sample.txt        # Sample text file for testing
├── __init__.py       # Package initialization
└── README.md         # This file
```

## Installation

No installation required. Simply clone or download the files and ensure Python 3.7+ is installed on your system.

## Usage

### Basic Word Counting

Count the top 5 most frequent words (default):
```bash
python3 main.py sample.txt
```

Count top N words:
```bash
python3 main.py sample.txt 10
```

### Search Specific Words

Search for specific words in the file:
```bash
python3 main.py sample.txt --search hello world sample
```

### Log Level Filtering

Extract log entries by specific log level:
```bash
python3 main.py logfile.txt --level_log ERROR
python3 main.py logfile.txt --level_log DEBUG
```

## Examples

### Example 1: Word Frequency Analysis
```bash
python3 main.py sample.txt 3
```
Output:
```
hello : 2
world : 2
sample : 2
```

### Example 2: Searching Specific Words
```bash
python3 main.py logs.text --search error failed
```
Output:
```
error : 3
failed : 2
```

### Example 3: Multiple Word Search with Mixed Case
```bash
python3 main.py logs.text --search ERROR INFO database
```
Output:
```
error : 3
info : 2
database : 2
```

### Example 4: Log Level Filtering
```bash
python3 main.py logs.text --level_log ERROR
```
Output:
```
Log Entries for ERROR (Timestamp, Log Level):
2025-07-30 21:15:15,456 : ERROR
2025-07-30 21:15:30,678 : ERROR
```

## Log File Format

The tool expects log files to follow this timestamp format:
```
YYYY-MM-DD HH:MM:SS,mmm LEVEL message
```

Example (from `logs.text`):
```
2025-07-30 21:15:01,234 INFO  [main] com.example.Application - Application started successfully.
2025-07-30 21:15:15,456 ERROR [data-processor-2] com.example.DataProcessor - Failed to process record ID: 12345.
2025-07-30 21:15:30,678 ERROR [database-connection] com.example.DatabaseManager - Database connection failed.
```

## API Reference

### Main Module (`main.py`)
- Entry point for CLI interface
- File path handling and error management
- Delegates processing to CLI handler

### CLI Handler Module (`cli.py`)
- `CLIHandler` class with static methods:
  - `parse_args_and_run(lines)`: Parse command line arguments and execute appropriate functionality
  - `print_top_words(result)`: Format and display word frequency results
  - `print_search_results(result)`: Format and display search results
  - `print_log_entries(log_level, entries)`: Format and display filtered log entries
- Handles argument parsing for word counting, searching, and log filtering
- Provides consistent output formatting across all operations

### Counter Module (`counter.py`)
- `WordCounter` class:
  - `count_top_words(top_n)`: Count and return top N most frequent words
  - `search_specific_words(search_words, log_level)`: Search for specific words with optional log level filtering
- Word frequency analysis and counting utilities
- Case-insensitive word matching

### Processor Module (`processor.py`)
- `LogProcessor` class:
  - `get_log_entries_by_level(log_level)`: Extract and return log entries for a specific level
- Log filtering and processing operations
- Advanced log analysis functions

### Parser Module (`parser.py`)
- `LogParser` class with static methods:
  - `read_file(file_path)`: Read and return file lines
  - `extract_words(text)`: Extract words using regex
  - `parse_log_entry(line)`: Parse timestamp and log level from log line

### LogEntry DataClass (`parser.py`)
Represents a parsed log entry with:
- `timestamp`: String representation of the log timestamp
- `loglevel`: Log level (ERROR, DEBUG, INFO, etc.)

## Module Architecture

The project follows a modular design pattern with clear separation of concerns:

- **`main.py`**: Application entry point and file handling
- **`cli.py`**: Command-line interface and argument parsing logic
- **`parser.py`**: Core parsing utilities and data structures
- **`counter.py`**: Word counting and frequency analysis logic
- **`processor.py`**: Log processing and filtering operations

### Key Benefits of This Architecture:
- **Single Responsibility**: Each module has a specific purpose
- **Loose Coupling**: Modules interact through well-defined interfaces
- **Easy Testing**: Individual components can be tested in isolation
- **Code Reusability**: Modules can be reused in other projects
- **Maintainability**: Changes in one module don't affect others
- **Extensibility**: New features can be added without modifying existing code

## Error Handling

The tool includes comprehensive error handling for:
- **File Access**: File not found errors and permission errors
- **Input Validation**: Invalid command-line arguments and malformed parameters
- **Data Processing**: Malformed log entries and encoding issues
- **User Feedback**: Clear error messages and usage instructions
- **Graceful Degradation**: Continues processing when encountering invalid log entries

### CLI Error Handling Features:
- Validates required arguments before processing
- Provides helpful usage messages for incorrect syntax
- Handles edge cases like empty search terms or invalid numbers
- Exits gracefully with appropriate error codes

## Testing

Test the basic functionality with the included sample files:

### Word Frequency Analysis
```bash
python3 main.py sample.txt
python3 main.py sample.txt 5
python3 main.py logs.text 10
```

### Word Search Functionality
```bash
python3 main.py logs.text --search error
python3 main.py logs.text --search ERROR failed database
python3 main.py sample.txt --search hello world
```

### Log Level Filtering
```bash
python3 main.py logs.text --level_log ERROR
python3 main.py logs.text --level_log INFO
python3 main.py logs.text --level_log DEBUG
```

### Edge Cases and Error Handling
```bash
# Test with invalid file
python3 main.py nonexistent.txt

# Test with invalid arguments
python3 main.py logs.text --search

# Test with invalid number
python3 main.py logs.text -5
```

## Performance Considerations

- **Efficient File Processing**: Reads files line by line to handle large log files
- **Memory Optimization**: Uses Counter for efficient word counting
- **Regex Performance**: Optimized regex patterns for fast text processing
- **Modular Design**: Allows for easy performance optimization of individual components
- **Case-Insensitive Search**: Efficient lowercase conversion for consistent matching
- **Early Exit Patterns**: Validates inputs early to avoid unnecessary processing

## Related Projects

This log analyzer is part of a larger collection of Python tools and examples. Check out the [YouTube playlist](https://www.youtube.com/watch?v=mnyV68QtmWM&list=PLZdyjUgq8p7k8BV9JMxfNyR3g7BVGioAl) for demonstrations and tutorials.

## Contributing

This project is part of a learning portfolio. Feel free to suggest improvements or report issues. When contributing:

1. **Maintain Architecture**: Preserve the modular design and separation of concerns
2. **Follow Standards**: Add appropriate error handling and include docstrings for new functions
3. **Test Thoroughly**: Test with both sample files (sample.txt and logs.text)
4. **Update Documentation**: Update README when adding new features or modules
5. **CLI Consistency**: Ensure new CLI features follow the existing argument parsing patterns

### Development Guidelines:
- Use static methods in CLI handler for consistency
- Follow the existing error handling patterns
- Maintain backward compatibility with existing command syntax
- Add comprehensive testing for new functionality

## License

This project is part of the [Command & Code Playground](../../../README.md) and is intended for educational purposes.

## Future Enhancements

- **Configuration Support**: Add configuration file support for default settings
- **Advanced Parsing**: Implement more sophisticated log parsing patterns for different log formats
- **Export Functionality**: Add export capabilities (JSON, CSV, XML formats)
- **Performance Metrics**: Include processing time and memory usage statistics
- **Unit Testing**: Add comprehensive unit tests for all modules including CLI handler
- **Interactive Mode**: Add interactive CLI mode for exploratory data analysis
- **Filtering Combinations**: Support combining multiple filters (e.g., date range + log level)
- **Visualization**: Add basic text-based charts for word frequency distribution