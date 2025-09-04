import sys

# Import from the parser
from parser import LogParser
from cli import CLIHandler

# Driver code
if __name__ == "__main__":
    # Passing the file path in the terminal when exucting the program/script
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <file_path> [top_n | --search word1 word2 ... [--level_log LEVEL]")
        sys.exit(1)

    # Get the file path
    file_path = sys.argv[1]
    try:
        lines = LogParser.read_file(file_path)
        CLIHandler.parse_args_and_run(lines)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)