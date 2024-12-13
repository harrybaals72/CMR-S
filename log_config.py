import logging
import sys
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define custom log levels
TRACE_LEVEL_NUM = 5
VERBOSE_LEVEL_NUM = 15

logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")
logging.addLevelName(VERBOSE_LEVEL_NUM, "VERBOSE")

def trace(self, message, *args, **kws):
    if self.isEnabledFor(TRACE_LEVEL_NUM):
        self._log(TRACE_LEVEL_NUM, message, args, **kws)

def verbose(self, message, *args, **kws):
    if self.isEnabledFor(VERBOSE_LEVEL_NUM):
        self._log(VERBOSE_LEVEL_NUM, message, args, **kws)

logging.Logger.trace = trace
logging.Logger.verbose = verbose

# Define color mappings for different log levels
class ColoredFormatter(logging.Formatter):
    COLORS = {
        TRACE_LEVEL_NUM: Fore.MAGENTA,
        VERBOSE_LEVEL_NUM: Fore.CYAN,
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, Fore.WHITE)
        record.levelname = color + record.levelname + Style.RESET_ALL
        return super().format(record)

def configure_logging(log_level=logging.INFO, log_file="app.log"):
    # Create a custom formatter
    formatter = ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Create a file handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)

    # Configure the root logger
    logging.basicConfig(level=log_level, handlers=[console_handler, file_handler])
    