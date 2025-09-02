import sys

class CLIHandler:
    @staticmethod
    def print_top_words(result):
        """Use to print the top word frequencies"""
        for word, count in result:
            print(f"{word} : {count}")

    @staticmethod
    def print_search_results(result):
        """Use to print the search words"""
        for word, count in result:
            print(f"{word} : {count}")

    @staticmethod
    def print_log_entries(log_level, entries):
        """Use to print log entries"""
        print(f"Log entries for {log_level.upper()} (Timestamp, Log Level):")
        if entries:
            for entry in entries:
                print(f"{entry.timestamp} : {entry.loglevel}")
        else:
            print(f"Yo, no log level found for {log_level.upper()}")

    @staticmethod
    def parse_args_and_run(lines):
        """Use to check and proceed the user cli input"""
        args = sys.argv
        
        if len(args) < 2:
            print("Usage: python3 main.py <file_path> [top_n | --search word1 word2 ... | --level_log LEVEL]")
            sys.exit(1)

        args = sys.argv[1:] # Ignore script name, file_path is args[0]

        if len(args) >= 2 and args[1] == '--search':
            search_words = []
            log_level = None
            i = 2
            while i < len(args):
                if args[i] == '--level_log':
                    if i + 1 < len(args):
                        log_level = args[i + 1]
                        i += 2
                    else:
                        print("Usage: --search word1 word2 ... [--level_log LEVEL]")
                        sys.exit(1)
                else:
                    search_words.append(args[i])
                    i += 1
            
            if not search_words:
                print("Please provide words to search after --search")
                sys.exit(1)
            
            counter = WordCounter(lines)
            result = counter.search_specific_words(search_words, log_level)
            CLIHandler.print_search_results(result)
            
        else:
            try:
                top_n = int(args[1]) if len(args) >= 2 else 5
                if top_n <= 0:
                    print("Top N must be a positive integer")
                    sys.exit(1)
            except ValueError:
                print("Invalid number provided for top_n")
                sys.exit(1)
            
            counter = WordCounter(lines)
            result = counter.count_top_words(top_n)
            CLIHandler.print_top_words(result)