import logging
import sys

from mindee.v2.commands.cli_parser import MindeeParser

_V1_DASHV_PRODUCTS = ("custom", "generated")


def _find_v1_dashv_boundary(argv: list[str]) -> int | None:
    """Locate the position after which ``-v`` belongs to V1 ``custom`` /
    ``generated``.

    These two V1 products register ``-v/--version``; tokens at or beyond
    the returned index must be left alone by the verbose pre-scan.
    """
    for i, token in enumerate(argv):
        if token == "v1" and i + 1 < len(argv) and argv[i + 1] in _V1_DASHV_PRODUCTS:
            return i + 2
    return None


def _extract_verbose_level(argv: list[str]) -> tuple[int, list[str]]:
    """Pre-scan ``argv`` for ``--verbose`` / ``-v`` flags.

    Mirrors ``mindee-api-dotnet``'s ``args.Contains("--verbose")`` check:
    the flag is consumed before argparse runs so it can appear anywhere
    on the command line.

    * ``--verbose`` is consumed at any position (no conflict).
    * ``-v`` is consumed at any position *except* after a ``v1 custom``
      or ``v1 generated`` invocation, where it is the V1 product's own
      ``--version`` option.

    :returns: ``(level, remaining_argv)`` where ``level`` counts the number
        of recognized verbose-flag occurrences.
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
    """Set the ``mindee`` logger level based on the verbose count."""
    if verbose_level <= 0:
        return
    target = logging.INFO if verbose_level == 1 else logging.DEBUG
    logging.getLogger("mindee").setLevel(target)
    logging.getLogger().setLevel(target)


def main() -> None:
    """Run the Command Line Interface.

    The unified ``mindee`` binary exposes V2 inference commands and the
    ``search-models`` utility at the root, with all V1 product commands
    wrapped under a ``v1`` subcommand — mirroring the canonical
    ``mindee-api-dotnet`` CLI.

    Pass ``--verbose`` (or ``-v``) to enable diagnostic logging; repeat
    the flag (``--verbose --verbose``) for debug-level output.
    """
    verbose_level, argv = _extract_verbose_level(sys.argv[1:])
    _configure_logging(verbose_level)
    sys.argv = [sys.argv[0], *argv]
    parser = MindeeParser()
    sys.exit(parser.call_parse() or 0)
