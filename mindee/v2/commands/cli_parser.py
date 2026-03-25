from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from typing import Optional, Type, Union

from mindee import (
    ClientV2,
    InferenceResponse,
    CropResponse,
    SplitResponse,
    ClassificationResponse,
    InferenceParameters,
    ClassificationParameters,
    CropParameters,
    SplitParameters,
)
from mindee.input import BaseParameters

from mindee.input.sources import PathInput, UrlInputSource
from mindee.v2.parsing import BaseResponse


@dataclass
class ProductConfig:
    """Configuration for a command."""

    response_class: Type[BaseResponse]
    params_class: Type[BaseParameters]


PRODUCTS = {
    "classification": ProductConfig(
        response_class=ClassificationResponse,
        params_class=ClassificationParameters,
    ),
    "crop": ProductConfig(
        response_class=CropResponse,
        params_class=CropParameters,
    ),
    "extraction": ProductConfig(
        response_class=InferenceResponse,
        params_class=InferenceParameters,
    ),
    "split": ProductConfig(
        response_class=SplitResponse,
        params_class=SplitParameters,
    ),
}


class MindeeArgumentParser(ArgumentParser):
    """Custom parser to simplify adding various options."""

    def add_main_options(self) -> None:
        """Adds main options for most parsings."""
        self.add_argument(
            "-k",
            "--key",
            dest="api_key",
            help="API key for the account",
            required=False,
            default=None,
        )
        self.add_argument(
            "-m",
            "--model-id",
            dest="model_id",
            help="Model ID",
            required=True,
            default=None,
        )

    def add_path_arg(self) -> None:
        """Adds options related to output/display of a document (parse, parse-queued)."""
        self.add_argument(dest="path", help="Full path to the file")


class MindeeParser:
    """Custom parser for the Mindee CLI."""

    parser: MindeeArgumentParser
    """Parser options."""
    parsed_args: Namespace
    """Stores attributes relating to parsing."""
    client: ClientV2
    """Mindee client"""
    input_source: Union[PathInput, UrlInputSource]
    """Document to be parsed."""

    def __init__(
        self,
        parser: Optional[MindeeArgumentParser] = None,
        parsed_args: Optional[Namespace] = None,
        client: Optional[ClientV2] = None,
    ) -> None:
        self.parser = (
            parser if parser else MindeeArgumentParser(description="Mindee_API")
        )
        self.parsed_args = parsed_args if parsed_args else self._set_args()
        if client:
            self.client = client
        else:
            api_key = self.parsed_args.api_key if "api_key" in self.parsed_args else ""
            self.client = ClientV2(api_key=api_key)
        self.input_source = self._get_input_source()

    def call_parse(self) -> None:
        """Calls the parse method of the input document."""
        product_conf = PRODUCTS[self.parsed_args.product_name]
        response = self.client.enqueue_and_get_result(
            response_type=product_conf.response_class,
            input_source=self.input_source,
            params=product_conf.params_class(
                model_id=self.parsed_args.model_id,
            ),
        )
        print(response.inference)

    def _set_args(self) -> Namespace:
        """Parse command line arguments."""
        parse_product_subparsers = self.parser.add_subparsers(
            dest="product_name",
            required=True,
        )
        for name in PRODUCTS:
            parse_subparser = parse_product_subparsers.add_parser(name)

            parse_subparser.add_main_options()
            parse_subparser.add_path_arg()

        parsed_args = self.parser.parse_args()
        return parsed_args

    def _get_input_source(self) -> Union[PathInput, UrlInputSource]:
        """Loads an input document."""

        if self.parsed_args.path.lower().startswith("http"):
            return UrlInputSource(self.parsed_args.path)
        return PathInput(self.parsed_args.path)
