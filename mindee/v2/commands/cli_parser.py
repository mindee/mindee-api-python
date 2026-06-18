import sys
from argparse import ArgumentParser, Namespace
from collections.abc import Callable

from mindee.v1.commands.cli_parser import (
    MindeeParser as V1MindeeParser,
)
from mindee.v1.commands.cli_parser import (
    register_v1_product_subparsers,
)
from mindee.v1.error.mindee_api_error import MindeeAPIError
from mindee.v2.client import Client
from mindee.v2.commands.inference_command import (
    InferenceCommand,
    InferenceCommandOptions,
)
from mindee.v2.commands.search_models_command import SearchModelsCommand
from mindee.v2.error.mindee_api_v2_error import MindeeAPIV2Error

PROG_NAME = "mindee"
"""Program name displayed in usage strings and help output."""


class MindeeArgumentParser(ArgumentParser):
    """Top-level argument parser for the unified ``mindee`` CLI."""


_INFERENCE_COMMANDS: list[InferenceCommand] = [
    InferenceCommand(
        InferenceCommandOptions(
            name="classification",
            description="Classification utility.",
        )
    ),
    InferenceCommand(
        InferenceCommandOptions(
            name="crop",
            description="Crop utility.",
        )
    ),
    InferenceCommand(
        InferenceCommandOptions(
            name="extraction",
            description="Generic all-purpose extraction.",
            rag=True,
            raw_text=True,
            confidence=True,
            polygon=True,
            text_context=True,
        )
    ),
    InferenceCommand(
        InferenceCommandOptions(
            name="ocr",
            description="OCR utility.",
        )
    ),
    InferenceCommand(
        InferenceCommandOptions(
            name="split",
            description="Split utility.",
        )
    ),
]


class MindeeParser:
    """
    Top-level parser for the unified ``mindee`` CLI.

    The shape mirrors the .NET ``Mindee.Cli`` binary:

    * V2 inference commands are exposed at the root level
      (``classification``, ``crop``, ``extraction``, ``ocr``, ``split``).
    * The ``search-models`` utility is also at the root.
    * V1 product commands are wrapped under a ``v1`` subcommand.
    """

    parser: MindeeArgumentParser
    parsed_args: Namespace
    _client_factory: Callable[[str | None], Client]
    _inference_commands: dict[str, InferenceCommand]
    _search_models_command: SearchModelsCommand

    def __init__(
        self,
        parser: MindeeArgumentParser | None = None,
        parsed_args: Namespace | None = None,
        client_factory: Callable[[str | None], Client] | None = None,
    ) -> None:
        self.parser = (
            parser
            if parser
            else MindeeArgumentParser(prog=PROG_NAME, description="Mindee CLI")
        )
        self._inference_commands = {
            cmd.options.name: cmd for cmd in _INFERENCE_COMMANDS
        }
        self._search_models_command = SearchModelsCommand()
        if parsed_args is None:
            self._build_parser()
            self.parsed_args = self.parser.parse_args()
        else:
            self.parsed_args = parsed_args
        self._client_factory = client_factory or _default_client_factory

    def call_parse(self) -> int:
        """Dispatch the parsed command to its handler.

        :returns: The exit code (``0`` on success, ``1`` on a recoverable
            CLI error such as a missing API key).
        """
        cmd = getattr(self.parsed_args, "cmd", None)
        if cmd is None:
            print("Please specify a subcommand.\n")
            self.parser.print_help()
            return 1
        try:
            if cmd == "v1":
                v1_parser = V1MindeeParser(parsed_args=self.parsed_args)
                v1_parser.call_parse()
                return 0
            if cmd == self._search_models_command.name:
                return self._search_models_command.execute(
                    self.parsed_args, self._client_factory
                )
            inference_command = self._inference_commands.get(cmd)
            if inference_command is None:
                raise ValueError(f"Unknown command: {cmd}")
            return inference_command.execute(self.parsed_args, self._client_factory)
        except MindeeAPIV2Error as exc:
            return _report_api_key_error(exc, "V2", "MINDEE_V2_API_KEY")
        except MindeeAPIError as exc:
            return _report_api_key_error(exc, "V1", "MINDEE_API_KEY")

    def _build_parser(self) -> None:
        # ``--verbose`` / ``-v`` are pre-consumed in ``mindee.cli.main``
        # (mirroring the .NET ``args.Contains("--verbose")`` pattern); we
        # still register them here for ``--help`` discoverability.
        self.parser.add_argument(
            "-v",
            "--verbose",
            action="count",
            default=0,
            help="Enable diagnostic logging (repeat for debug-level output).",
        )
        subparsers = self.parser.add_subparsers(dest="cmd", required=False)

        for cmd in self._inference_commands.values():
            cmd.register(subparsers)

        self._search_models_command.register(subparsers)

        v1_parser = subparsers.add_parser(
            "v1",
            help="Mindee V1 product commands.",
            description="Mindee V1 product commands.",
        )
        register_v1_product_subparsers(v1_parser)


def _default_client_factory(api_key: str | None) -> Client:
    return Client(api_key=api_key) if api_key else Client()


def _report_api_key_error(exc: Exception, version: str, env_var: str) -> int:
    """Print a friendly missing-key message to stderr and return exit code 1.

    Mirrors the .NET CLI's handling of ``OptionsValidationException`` when
    the API key cannot be resolved from the command line or the environment.
    """
    message = str(exc) or "API key is missing."
    if "Missing API key" in message or "api key" in message.lower():
        message = (
            f"The Mindee {version} API key is missing. "
            f"Please provide it via the '--api-key' option "
            f"or the '{env_var}' environment variable."
        )
    print(f"Error: {message}", file=sys.stderr)
    return 1
