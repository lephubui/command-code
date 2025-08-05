# Parser to analyze log files from logs.text
import re

def parse_log_file(file_path):
    """
    Parses a log file and returns a list of dictionaries with log details.
    
    Args:
        file_path (str): Path to the log file.
        
    Returns:
        list: A list of dictionaries containing parsed log entries.
    """
    log_entries = []
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Example regex pattern to match log entries
                match = re.match(r'(?P<timestamp>\S+) (?P<level>\S+) (?P<message>.*)', line)
                if match:
                    log_entries.append(match.groupdict())
    except FileNotFoundError as e:
        print(f"Error: {e}")
    
    return log_entries