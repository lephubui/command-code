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

## System Requirements

- **Operating System**: Ubuntu 24.04 (tested and optimized)
- **Python Version**: 3.7+
- **Dependencies**: No external dependencies for core functionality

## Project Structure

```
log_analyzer/
├── main.py           # Main application with CLI interface
├── parser.py         # Log parsing utilities and data structures
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
python3 main.py sample.txt --search hello world
```
Output:
```
hello : 2
world : 2
```

### Example 3: Log Level Filtering
```bash
python3 main.py app.log --level_log ERROR
```
Output:
```
Log Entries for ERROR (Timestamp, Log Level):
2024-01-15 10:30:45,123 : ERROR
2024-01-15 11:45:22,456 : ERROR
```

## Log File Format

The tool expects log files to follow this timestamp format:
```
YYYY-MM-DD HH:MM:SS,mmm LEVEL message
```

Example:
```
2024-01-15 10:30:45,123 ERROR Database connection failed
2024-01-15 10:30:46,124 INFO Retrying connection
2024-01-15 10:30:47,125 DEBUG Connection parameters: host=localhost
```

## API Reference

### Core Functions

- `count_words(file_path, top_n_input)`: Count word frequencies
- `search_specific_words(file_path, search_words, log_level)`: Search for specific words
- `process_log(file_path, level_log)`: Extract log entries by level

### LogParser Class

- `read_file(file_path)`: Read and return file lines
- `extract_words(text)`: Extract words using regex
- `parse_log_entry(line)`: Parse timestamp and log level from log line

### LogEntry DataClass

Represents a parsed log entry with:
- `timestamp`: String representation of the log timestamp
- `loglevel`: Log level (ERROR, DEBUG, INFO, etc.)

## Error Handling

The tool includes comprehensive error handling for:
- File not found errors
- Permission errors
- Invalid input formats
- Missing command-line arguments

## Testing

Test the basic functionality with the included sample file:
```bash
python3 main.py sample.txt
python3 main.py sample.txt --search hello world
```

## Related Projects

This log analyzer is part of a larger collection of Python tools and examples. Check out the [YouTube playlist](https://www.youtube.com/watch?v=mnyV68QtmWM&list=PLZdyjUgq8p7k8BV9JMxfNyR3g7BVGioAl) for demonstrations and tutorials.

## Contributing

This project is part of a learning portfolio. Feel free to suggest improvements or report issues.

## License

This project is part of the [Command & Code Playground](cc/command-code/README.md) and is intended for educational