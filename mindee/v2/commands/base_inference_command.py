from abc import abstractmethod
from argparse import ArgumentParser, Namespace, _SubParsersAction
from collections.abc import Callable

from mindee import (
    ClassificationResponse,
    CropResponse,
    ExtractionResponse,
    OCRResponse,
    SplitResponse,
)
from mindee.input import PathInput, URLInputSource
from mindee.v2.client import Client
from mindee.v2.client_options.base_product_parameters import BaseProductParameters
from mindee.v2.commands.output_type import OutputType


class BaseInferenceCommand:
    """Abstract base class for V2 inference CLI commands."""

    name: str
    """Name of the subcommand (also used as product key)."""

    description: str
    """Human-readable description shown in the help."""

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
            "-m",
            "--model-id",
            dest="model_id",
            help="ID of the model to use.",
            required=True,
        )
        parser.add_argument(
            "-a",
            "--alias",
            dest="alias",
            help="Alias for the file.",
            required=False,
            default=None,
        )
        parser.add_argument(
            "-o",
            "--output",
            dest="output",
            choices=[item.value for item in OutputType],
            default=OutputType.SUMMARY.value,
            help=(
                "Specify how to output the data.\n"
                "- summary: a basic summary (default)\n"
                "- full: detailed extraction results, including options\n"
                "- raw: full JSON object\n"
            ),
        )
        parser.add_argument(
            "-w",
            "--webhook-id",
            dest="webhook_ids",
            action="append",
            help="Specify a webhook by ID. May be used multiple times.",
            required=False,
            default=None,
        )
        self.configure_product_options(parser)
        parser.add_argument("path", help="The path of the file to parse.")
        return parser

    def configure_product_options(self, parser: ArgumentParser) -> None:
        """Hook for subclasses to add product-specific options."""

    def execute(
        self,
        parsed_args: Namespace,
        client_factory: Callable[[str | None], Client],
    ) -> int:
        """Run the inference and print the result."""
        api_key = getattr(parsed_args, "api_key", None)
        model_id = parsed_args.model_id
        webhook_ids = getattr(parsed_args, "webhook_ids", None)
        alias = getattr(parsed_args, "alias", None)
        output_type = OutputType(
            getattr(parsed_args, "output", OutputType.SUMMARY.value)
        )

        client = client_factory(api_key)
        params = self.build_parameters(parsed_args, model_id, alias, webhook_ids)
        input_source = _build_input_source(parsed_args.path)
        response: (
            ExtractionResponse
            | CropResponse
            | ClassificationResponse
            | SplitResponse
            | OCRResponse
        ) = client.enqueue_and_get_result(
            response_type=self.get_response_class(),
            input_source=input_source,
            params=params,
        )
        self._print_response(parsed_args, response, output_type)
        return 0

    @abstractmethod
    def build_parameters(
        self,
        parsed_args: Namespace,
        model_id: str,
        alias: str | None,
        webhook_ids: list[str] | None,
    ) -> BaseProductParameters:
        """Build the V2 inference parameters for this product."""

    @abstractmethod
    def get_response_class(self) -> type:
        """Return the product response class to deserialize the API result into."""

    def get_summary(self, response) -> str:
        """Default human-readable representation of an inference response."""
        inference = getattr(response, "inference", None)
        if inference is None:
            return ""
        return str(inference.result)

    def get_full_output(self, parsed_args: Namespace, response) -> str:
        """Detailed representation of an inference response."""
        del parsed_args
        inference = getattr(response, "inference", None)
        if inference is None:
            return ""
        return str(inference)

    def _print_response(
        self,
        parsed_args: Namespace,
        response,
        output_type: OutputType,
    ) -> None:
        if output_type is OutputType.RAW:
            print(response.raw_http)
            return
        if output_type is OutputType.FULL:
            print(self.get_full_output(parsed_args, response))
            return
        print(self.get_summary(response))


def _build_input_source(path: str) -> PathInput | URLInputSource:
    if path.lower().startswith("http"):
        return URLInputSource(path)
    return PathInput(path)
