from argparse import ArgumentParser, Namespace, _SubParsersAction
from collections.abc import Callable

from mindee.v2.client import Client
from mindee.v2.search.rag_documents.rag_document_search_parameters import (
    RagDocumentSearchParameters,
)


class SearchRagDocumentsCommand:
    """CLI command for searching available RAG documents for a given model."""

    name = "search-rag-docs"
    description = "Search available RAG documents for a given model."

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
            help="Filter by model ID",
            required=True,
        )
        parser.add_argument(
            "-f",
            "--filename",
            dest="filename",
            help="Filter by file name partial match (case insensitive).",
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
        response = client.search(
            RagDocumentSearchParameters(
                model_id=parsed_args.model_id,
                filename=getattr(parsed_args, "filename", None),
            )
        )
        if getattr(parsed_args, "raw_json", False):
            print(response.raw_http)
        else:
            print(response)
        return 0
