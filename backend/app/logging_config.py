import logging
import sys


class ColorFormatter(logging.Formatter):
    """Console ke liye colored log levels — taaki terminal mein easily scan ho sake."""

    COLORS = {
        "DEBUG": "\033[36m",     # cyan
        "INFO": "\033[32m",      # green
        "WARNING": "\033[33m",   # yellow
        "ERROR": "\033[31m",     # red
        "CRITICAL": "\033[41m",  # red background
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        record.levelname = f"{color}{record.levelname:<8}{self.RESET}"
        return super().format(record)


def setup_logging(level: int = logging.INFO) -> None:
    """App startup pe ek baar call karo (main.py mein). Duplicate handlers na lagein
    isliye agar root logger already configured hai toh skip kar dete hain (uvicorn --reload ke liye zaroori)."""
    root = logging.getLogger()

    if root.handlers:
        return

    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    formatter = ColorFormatter(
        fmt="%(asctime)s | %(levelname)s | %(name)-30s | %(message)s",
        datefmt="%H:%M:%S",
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)

    # Third-party libraries bahut zyada noisy hoti hain — inhe warning level pe rakho
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)