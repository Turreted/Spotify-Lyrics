import logging
import argparse


"""
Purpose of File is defined here
"""


def init_logger(log_level: str) -> logging.Logger:
    """
    Define the logging.Logger used to debug the application.

    Parameters
    ________

    log_level: str
        the debugging level used by the application.
        May be one of "INFO", "DEBUG", or "ERROR"


    Outputs
    _______
    logger: logging.Logger
        the logger class with the specified debug level
    """

    logger = logging.getLogger(__name__)
    formatter = logging.Formatter(fmt="{asctime} - {levelname} - {message}", style="{")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.setLevel(log_level)
    return logger


def init_argparser() -> argparse.ArgumentParser:
    """
    Sets up an argparse.ArgumentParser in order to handle
    user input. If credentials are not found in the argparser
    or in environment variables, the user is prompted.

    TODO: add creds as arguments

    Outputs
    _______
    argparser: argparse.Argparser
        the argparser class with all command line arguments
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log",
        help="set the log level",
        choices=["INFO", "DEBUG", "ERROR"],
        default="ERROR",
    )

    return parser
