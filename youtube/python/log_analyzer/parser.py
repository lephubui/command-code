import re
from dataclasses import dataclass

@dataclass
class LogEntry:
    timestamp: str
    loglevel: str

class LogParser:
    def read_file(file_path):
        """Define how to read a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.readlines()
        except (FileNotFoundError, PermissionError) as err:
            print(f"Error accessing file: {err}")
            raise # Raise to handle in caller

    def extract_words(text):
        """Extract words from text using regex"""
        return re.findall(r'\b\w+\b', text.lower())

    def parse_log_entry(line):
        """Parse timestamp and log level from a log line."""
        match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s+(\w+)', line)
        if match:
            return LogEntry(timestamp=match.group(1), loglevel=match.group(2).upper())
        else:
            return None
