import sys
from typing import List, Tuple, Optional

from counter import WordCounter
from parser import  LogEntry


class CLIHandler:
    """Command Line Interface handler for the Log Analyzer application."""
    
    @staticmethod
    def print_results(result: List[Tuple[str, int]], prefix: str = "") -> None:
        """Print results in a consistent format."""
        if prefix:
            print(prefix)
        
        if result:
            for word, count in result:
                print(f"{word} : {count}")
        else:
            print("No results found")

    @staticmethod
    def print_log_entries(log_level: str, entries: List[LogEntry]) -> None:
        """Print log entries with timestamps and log levels."""
        print(f"Log entries for {log_level.upper()} (Timestamp, Log Level):")
        if entries:
            for entry in entries:
                print(f"{entry.timestamp} : {entry.loglevel}")
        else:
            print(f"No log level found for {log_level.upper()}")

    @staticmethod
    def _parse_search_args(args: List[str]) -> Tuple[List[str], Optional[str]]:
        """Parse search arguments and optional log level."""
        search_words = []
        log_level = None
        i = 1  # Skip '--search'
        
        while i < len(args):
            if args[i] == '--level_log':
                if i + 1 < len(args):
                    log_level = args[i + 1]
                    i += 2
                else:
                    raise ValueError("--level_log requires a value")
            else:
                search_words.append(args[i])
                i += 1
        
        if not search_words:
            raise ValueError("Please provide words to search after --search")
        
        return search_words, log_level

    @staticmethod
    def _parse_top_n(args: List[str]) -> int:
        """Parse and validate top_n argument."""
        if not args:
            return 5  # Default value
        
        try:
            top_n = int(args[0])
            if top_n <= 0:
                raise ValueError("Top N must be a positive integer")
            return top_n
        except ValueError as e:
            if "invalid literal" in str(e):
                raise ValueError("Invalid number provided for top_n")
            raise

    @staticmethod
    def _handle_search_command(args: List[str], lines: List[str]) -> None:
        """Handle search command with optional log level filtering."""
        try:
            search_words, log_level = CLIHandler._parse_search_args(args)
            counter = WordCounter(lines)
            result = counter.search_specific_words(search_words, log_level)
            CLIHandler.print_results(result)
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

    @staticmethod
    def _handle_count_command(args: List[str], lines: List[str]) -> None:
        """Handle word count command."""
        try:
            top_n = CLIHandler._parse_top_n(args)
            counter = WordCounter(lines)
            result = counter.count_top_words(top_n)
            CLIHandler.print_results(result)
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

    @staticmethod
    def parse_args_and_run(lines: List[str]) -> None:
        """Parse command line arguments and execute appropriate action."""
        args = sys.argv[2:]  # Skip script name and file_path
        
        if len(sys.argv) < 2:
            print("Usage: python3 main.py <file_path> [top_n | --search word1 word2 ... | --level_log LEVEL]")
            sys.exit(1)

        # Route to appropriate handler based on command
        if args and args[0] == '--search':
            CLIHandler._handle_search_command(args, lines)
        else:
            CLIHandler._handle_count_command(args, lines)