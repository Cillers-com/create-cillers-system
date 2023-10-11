import contextlib
from datetime import datetime
import logging
import os
import re

def colorize(text, color_code):
    """Wrap text with the ANSI escape code for the given color."""
    return f"\033[{color_code}m{text}\033[39m"

def bold(text):
    """Bold the given text."""
    return f"\033[1m{text}\033[22m"

def faint(text):
    """Faint the given text."""
    return f"\033[2m{text}\033[22m"

def italic(text):
    """Italicize the given text."""
    return f"\033[3m{text}\033[23m"

def black(text): return colorize(text, 30)
def red(text): return colorize(text, 31)
def green(text): return colorize(text, 32)
def yellow(text): return colorize(text, 33)
def blue(text): return colorize(text, 34)
def magenta(text): return colorize(text, 35)
def cyan(text): return colorize(text, 36)
def white(text): return colorize(text, 37)

CRITICAL = logging.CRITICAL
DEBUG = logging.DEBUG
ERROR = logging.ERROR
INFO = logging.INFO
TRACE = 5
WARNING = logging.WARNING

LEVEL_LABELS = {
    'CRITICAL': red(bold('CRITICAL')),
    'DEBUG': magenta('DEBUG'),
    'ERROR': red('ERROR'),
    'INFO': white('INFO'),
    'TRACE': green(faint(bold('TRACE'))),
    'WARNING': yellow('WARNING'),
}


def strip_ansi(s: str) -> str:
    r = re.compile(r'\x1B\[.*?[a-zA-Z]')
    return r.sub('', s)

def disp_len(s: str) -> int:
    return len(strip_ansi(s))

def indent_rest(input_string: str, indent: int) -> str:
    lines = input_string.split("\n")
    return "\n".join([lines[0]] + [f"{' ' * indent}{line}" for line in lines[1:]])

# NOTE: the Couchbase lib generates this annoying warning even though we're not using
#       max_ttl. This filter suppresses it.
class IgnoreMaxTTLWarningFilter(logging.Filter):
    def filter(self, record):
        if "max_ttl is deprecated" in record.getMessage():
            return False
        return True

class LowerHttpxLevelHandler(logging.StreamHandler):
    def emit(self, record):
        if record.name == 'httpx':
            level = record.levelno
            if level in {logging.INFO, logging.DEBUG}:
                record.levelno = TRACE if level == logging.DEBUG else logging.DEBUG
                record.levelname = 'TRACE' if level == logging.DEBUG else 'DEBUG'
        super().emit(record)

class Formatter(logging.Formatter):
    def format(self, record):
        ts = (datetime
              .utcfromtimestamp(record.created)
              .strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')
        level = LEVEL_LABELS.get(record.levelname, record.levelname)
        n = record.name
        color = sum([ord(x) for x in n]) % 6 + 32
        msg = record.getMessage()
        base = f"{italic(ts)} – {colorize(n, color)} – {level} – "
        return f"{base}{indent_rest(msg, disp_len(base))}"

def get_logger(name):
    return logging.getLogger(name)

def set_level(level):
    if level in logging._nameToLevel:
        logging.getLogger().setLevel(level)
    else:
        logging.getLogger(__name__).warning('Invalid log level %s; ignoring.',
                                            red(level))

def init():
    logging.captureWarnings(True)
    level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    logger = logging.getLogger()
    handler = LowerHttpxLevelHandler()
    handler.setFormatter(Formatter('%(message)s'))

    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('py.warnings').addFilter(IgnoreMaxTTLWarningFilter())

    logger.handlers = [handler]
    set_level(level)

@contextlib.contextmanager
def level(level):
    logger = logging.getLogger()
    old_level = logger.level
    logger.setLevel(level)
    try:
        yield  # Yield control back to the calling block
    finally:
        logger.setLevel(old_level)  # Restore the original log level
