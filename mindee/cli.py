import io
import logging
import sys
from typing import cast

from mindee.v2.commands.cli_parser import MindeeParser

_V1_DASHV_PRODUCTS = ("custom", "generated")


def _find_v1_dashv_boundary(argv: list[str]) -> int | None:
    """Find the index after which -v means --version for V1 custom/generated."""
    for i, token in enumerate(argv):
        if token == "v1" and i + 1 < len(argv) and argv[i + 1] in _V1_DASHV_PRODUCTS:
            return i + 2
    return None


def _extract_verbose_level(argv: list[str]) -> tuple[int, list[str]]:
    """
    Consume --verbose / -v flags before argparse runs.

    :return: The verbose level and the remaining arguments.
    """
    level = 0
    remaining: list[str] = []
    v1_dashv_start = _find_v1_dashv_boundary(argv)
    for i, token in enumerate(argv):
        if token == "--verbose":
            level += 1
            continue
        if token == "-v" and (v1_dashv_start is None or i < v1_dashv_start):
            level += 1
            continue
        remaining.append(token)
    return level, remaining


def _configure_logging(verbose_level: int) -> None:
    """Set the Mindee logger level based on the verbose count."""
    if verbose_level <= 0:
        return
    target = logging.INFO if verbose_level == 1 else logging.DEBUG
    logging.getLogger("mindee").setLevel(target)
    logging.getLogger().setLevel(target)


def main() -> None:
    """Run the Command Line Interface."""

    stdout = cast(io.TextIOWrapper, sys.stdout)
    stdout_encoding = str(stdout.encoding)
    if stdout_encoding and stdout_encoding.lower() != "utf-8":
        stdout.reconfigure(encoding="utf-8")
    verbose_level, argv = _extract_verbose_level(sys.argv[1:])
    _configure_logging(verbose_level)
    sys.argv = [sys.argv[0], *argv]
    parser = MindeeParser()
    sys.exit(parser.call_parse() or 0)
