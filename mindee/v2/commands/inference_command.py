from argparse import ArgumentParser, Namespace, _SubParsersAction
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from mindee import (
    ClassificationParameters,
    ClassificationResponse,
    CropParameters,
    CropResponse,
    ExtractionParameters,
    ExtractionResponse,
    OCRParameters,
    OCRResponse,
    SplitParameters,
    SplitResponse,
)
from mindee.input import PathInput, URLInputSource
from mindee.v2.client import Client
from mindee.v2.client_options.base_parameters import BaseParameters
from mindee.v2.commands.output_type import OutputType


@dataclass
class InferenceCommandOptions:
    """Configuration for a V2 inference subcommand."""

    name: str
    """Name of the subcommand (also used as product key)."""
    description: str
    """Human-readable description shown in ``--help``."""
    rag: bool = False
    """Whether to expose ``--rag/-g``."""
    raw_text: bool = False
    """Whether to expose ``--raw-text/-r``."""
    confidence: bool = False
    """Whether to expose ``--confidence/-c``."""
    polygon: bool = False
    """Whether to expose ``--polygon/-p``."""
    text_context: bool = False
    """Whether to expose ``--text-context/-t``."""


response_types_with_result = (
    ClassificationResponse
    | CropResponse
    | ExtractionResponse
    | OCRResponse
    | SplitResponse
)


@dataclass
class _ProductTypes:
    """Pair of response/parameter classes for a V2 inference product."""

    response_class: type[response_types_with_result]
    params_class: type[BaseParameters]


PRODUCTS: dict[str, _ProductTypes] = {
    "classification": _ProductTypes(
        response_class=ClassificationResponse,
        params_class=ClassificationParameters,
    ),
    "crop": _ProductTypes(
        response_class=CropResponse,
        params_class=CropParameters,
    ),
    "extraction": _ProductTypes(
        response_class=ExtractionResponse,
        params_class=ExtractionParameters,
    ),
    "ocr": _ProductTypes(
        response_class=OCRResponse,
        params_class=OCRParameters,
    ),
    "split": _ProductTypes(
        response_class=SplitResponse,
        params_class=SplitParameters,
    ),
}


@dataclass
class _InferenceArgs:
    """Bag of parsed CLI arguments for a V2 inference run."""

    product: str
    path: str
    model_id: str
    alias: str | None = None
    rag: bool = False
    raw_text: bool = False
    confidence: bool = False
    polygon: bool = False
    text_context: str | None = None
    output: OutputType = OutputType.SUMMARY
    api_key: str | None = None


class InferenceCommand:
    """Builder + handler for a V2 inference subcommand.

    Mirrors ``Mindee.Cli.Commands.V2.InferenceCommand`` from the .NET SDK:
    each command exposes ``--api-key/-k``, ``--model-id/-m``, ``--alias/-a``,
    ``--output/-o``, plus an opt-in subset of ``--rag/-g``, ``--raw-text/-r``,
    ``--confidence/-c``, ``--polygon/-p``, ``--text-context/-t``.
    """

    options: InferenceCommandOptions

    def __init__(self, options: InferenceCommandOptions) -> None:
        self.options = options

    def register(self, subparsers: _SubParsersAction) -> ArgumentParser:
        """Register this command on the given subparsers action."""
        parser = subparsers.add_parser(
            self.options.name,
            help=self.options.description,
            description=self.options.description,
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
        if self.options.rag:
            parser.add_argument(
                "-g",
                "--rag",
                dest="rag",
                action="store_true",
                help=(
                    "Enable Retrieval-Augmented Generation. "
                    "Only valid for the 'extraction' product."
                ),
            )
        if self.options.raw_text:
            parser.add_argument(
                "-r",
                "--raw-text",
                dest="raw_text",
                action="store_true",
                help="Extract the full text content from the document.",
            )
        if self.options.confidence:
            parser.add_argument(
                "-c",
                "--confidence",
                dest="confidence",
                action="store_true",
                help="Retrieve confidence scores for each field.",
            )
        if self.options.polygon:
            parser.add_argument(
                "-p",
                "--polygon",
                dest="polygon",
                action="store_true",
                help="Retrieve bounding-box polygons for each field.",
            )
        if self.options.text_context:
            parser.add_argument(
                "-t",
                "--text-context",
                dest="text_context",
                help="Additional text context used by the model during inference.",
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
        parser.add_argument("path", help="The path of the file to parse.")
        return parser

    def execute(
        self,
        parsed_args: Namespace,
        client_factory: Callable[[str | None], Client],
    ) -> int:
        """Run the inference for ``parsed_args`` using ``client_factory``."""
        args = _InferenceArgs(
            product=self.options.name,
            path=parsed_args.path,
            model_id=parsed_args.model_id,
            alias=getattr(parsed_args, "alias", None),
            rag=bool(getattr(parsed_args, "rag", False)),
            raw_text=bool(getattr(parsed_args, "raw_text", False)),
            confidence=bool(getattr(parsed_args, "confidence", False)),
            polygon=bool(getattr(parsed_args, "polygon", False)),
            text_context=getattr(parsed_args, "text_context", None),
            output=OutputType(getattr(parsed_args, "output", OutputType.SUMMARY.value)),
            api_key=getattr(parsed_args, "api_key", None),
        )
        client = client_factory(args.api_key)
        params = self._build_params(args)
        input_source = _build_input_source(args.path)
        response = client.enqueue_and_get_result(
            response_type=PRODUCTS[args.product].response_class,
            input_source=input_source,
            params=params,
        )
        _print_response(args, response)
        return 0

    def _build_params(self, args: _InferenceArgs) -> BaseParameters:
        cls = PRODUCTS[args.product].params_class
        kwargs: dict[str, Any] = {"model_id": args.model_id}
        if args.alias is not None:
            kwargs["alias"] = args.alias
        if cls is ExtractionParameters:
            if self.options.rag:
                kwargs["rag"] = args.rag
            if self.options.raw_text:
                kwargs["raw_text"] = args.raw_text
            if self.options.confidence:
                kwargs["confidence"] = args.confidence
            if self.options.polygon:
                kwargs["polygon"] = args.polygon
            if self.options.text_context and args.text_context is not None:
                kwargs["text_context"] = args.text_context
        return cls(**kwargs)


def _build_input_source(path: str) -> PathInput | URLInputSource:
    if path.lower().startswith("http"):
        return URLInputSource(path)
    return PathInput(path)


def _print_response(args: _InferenceArgs, response: response_types_with_result) -> None:
    if args.output is OutputType.RAW:
        print(response.raw_http)
        return
    if args.output is OutputType.FULL:
        inference = response.inference
        active_options = getattr(inference, "active_options", None)
        result = getattr(inference, "result", None)
        if (
            args.raw_text
            and active_options is not None
            and getattr(active_options, "raw_text", False)
            and result is not None
            and getattr(result, "raw_text", None) is not None
        ):
            print("#############\nRaw Text\n#############\n::\n")
            raw_text_str = str(result.raw_text).replace("\n", "\n  ")
            print("  " + raw_text_str + "\n")
        if (
            args.rag
            and active_options is not None
            and getattr(active_options, "rag", False)
            and result is not None
            and getattr(result, "rag", None) is not None
        ):
            print("#############\nRetrieval-Augmented Generation\n#############\n::\n")
            rag_str = str(result.rag).replace("\n", "\n  ")
            print("  " + rag_str + "\n")
        print(inference)
        return
    # default: summary
    print(response.inference.result)
