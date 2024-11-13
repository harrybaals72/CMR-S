import logging
import sys
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    # Define color mappings for different log levels
    COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        # Apply color to the log level name
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

# # Example usage of configuring logging
# if __name__ == '__main__':
#     configure_logging()
#     logger = logging.getLogger(__name__)
#     logger.debug("This is a debug message")
#     logger.info("This is an info message")
#     logger.warning("This is a warning message")
#     logger.error("This is an error message")
#     logger.critical("This is a critical message")