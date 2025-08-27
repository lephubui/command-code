from parser import LogParser, LogEntry

class LogProcessor:
    def __init__(self, lines):
        self.lines = lines

    def get_log_entries_by_level(self, log_level):
        """Get log entries for a specific log level."""
        log_entries = []
        for line in self.lines:
            entry = LogParser.parse_log_entry(line)
            if entry and entry.loglevel.lower() == log_level.lower():
                log_entries.append(entry)

        return log_entries

