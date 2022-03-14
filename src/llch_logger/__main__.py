import argparse

from . import Logger
from ._version import __version__

if __name__ == "__main__":
    levels = ["info", "warn", "error", "debug", "audit", "raw"]

    parser = argparse.ArgumentParser(
        description=f"""
    Sends logging messages [llch_logger {__version__}]

    By default, it sends an information message.
    """
    )

    parser.add_argument(
        "-m",
        "--message",
        type=str,
        help="Message to be sent. By default, it is of type information.",
    )

    group = parser.add_mutually_exclusive_group()
    for level in levels:
        group.add_argument(
            f"-{level[0].upper()}",
            f"--{level}",
            action="store_true",
            help=f"{level.upper()} message.",
        )

    parser.add_argument(
        "--config",
        type=str,
        default="./config.ini",
        help="Location of the configuration file. Default: ./config.ini",
    )

    args = parser.parse_args()

    logger = Logger(config_file=args.config)

    for level in levels:
        if getattr(args, level):
            getattr(logger, level)(args.message)
            break
    else:
        logger.info(args.message)
