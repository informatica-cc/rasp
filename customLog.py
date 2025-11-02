import os
from datetime import datetime


class Log:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_path = os.path.join(self.script_dir, "printer.log")

    def log(self, message: str):
        """Simple homemade logger that appends messages to printer.log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"{timestamp} | {message}\n"
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(line)
        except Exception as e:
            print(f"Logging failed: {e}")
