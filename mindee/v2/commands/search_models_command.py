from argparse import ArgumentParser, Namespace, _SubParsersAction
from collections.abc import Callable

from mindee.v2.client import Client

_AVAILABLE_MODEL_TYPES: list[str] = [
    "extraction",
    "crop",
    "classification",
    "ocr",
    "split",
]


class SearchModelsCommand:
    """Builder + handler for the V2 ``search-models`` subcommand.

    Mirrors ``Mindee.Cli.Commands.V2.SearchModelsCommand`` from the .NET
    SDK.
    """

    name = "search-models"
    description = "Search available models."

    def register(self, subparsers: _SubParsersAction) -> ArgumentParser:
        """Register this command on the given subparsers action."""
        parser = subparsers.add_parser(
            self.name,
            help=self.description,
            description=self.description,
        )
        parser.add_argument(
            "-k",
            "--api-key",
            dest="api_key",
            help="Mindee V2 API key.",
            required=False,
            default=None,
        )
        parser.add_argument(
            "-n",
            "--name",
            dest="name",
            help="Filter by model name partial match (case insensitive).",
            required=False,
            default=None,
        )
        model_type_help = (
            "Filter by exact model type (case sensitive).\nAvailable options:\n - "
            + "\n - ".join(_AVAILABLE_MODEL_TYPES)
        )
        parser.add_argument(
            "-m",
            "--model-type",
            dest="model_type",
            help=model_type_help,
            choices=_AVAILABLE_MODEL_TYPES,
            required=False,
            default=None,
        )
        parser.add_argument(
            "-r",
            "--raw-json",
            dest="raw_json",
            action="store_true",
            help="Whether to output the raw JSON response.",
        )
        return parser

    def execute(
        self,
        parsed_args: Namespace,
        client_factory: Callable[[str | None], Client],
    ) -> int:
        """Run the search and print the result."""
        client = client_factory(getattr(parsed_args, "api_key", None))
        response = client.search_models(
            name=getattr(parsed_args, "name", None),
            model_type=getattr(parsed_args, "model_type", None),
        )
        if getattr(parsed_args, "raw_json", False):
            print(response.raw_http)
        else:
            print(response)
        return 0
