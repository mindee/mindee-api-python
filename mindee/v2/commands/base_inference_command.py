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
from mindee.v2.client_options.base_parameters import BaseParameters
from mindee.v2.commands.output_type import OutputType


class BaseInferenceCommand:
    """Abstract base class for V2 inference CLI commands.

    Owns the options shared by every V2 inference product
    (``path``, ``--model-id``, ``--api-key``, ``--alias``, ``--output``),
    the input-source resolution, the client invocation, and the output
    formatting. Each concrete subclass owns its own product-specific
    options, builds the right :class:`BaseParameters` instance, and may
    customize the human-readable output.

    Mirrors the canonical PHP implementation in
    ``mindee-api-php/bin/V2/BaseInferenceCommand.php``.
    """

    name: str
    """Name of the subcommand (also used as product key)."""

    description: str
    """Human-readable description shown in ``--help``."""

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
        self.configure_product_options(parser)
        parser.add_argument("path", help="The path of the file to parse.")
        return parser

    def configure_product_options(self, parser: ArgumentParser) -> None:
        """Hook for subclasses to add product-specific options.

        No-op by default. Override (for example in
        :class:`~mindee.v2.commands.extraction_command.ExtractionCommand`)
        to add flags only relevant to a single product.
        """

    def execute(
        self,
        parsed_args: Namespace,
        client_factory: Callable[[str | None], Client],
    ) -> int:
        """Run the inference for ``parsed_args`` using ``client_factory``."""
        api_key = getattr(parsed_args, "api_key", None)
        model_id = parsed_args.model_id
        alias = getattr(parsed_args, "alias", None)
        output_type = OutputType(
            getattr(parsed_args, "output", OutputType.SUMMARY.value)
        )

        client = client_factory(api_key)
        params = self.build_parameters(parsed_args, model_id, alias)
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
    ) -> BaseParameters:
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
        """Detailed representation of an inference response.

        Defaults to the full inference dump; override to add
        product-specific sections (raw text, RAG, ...).
        """
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
