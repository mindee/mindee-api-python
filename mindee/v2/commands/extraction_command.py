from argparse import ArgumentParser, Namespace

from mindee import ExtractionParameters, ExtractionResponse
from mindee.v2.client_options.base_parameters import BaseParameters
from mindee.v2.commands.base_inference_command import BaseInferenceCommand


class ExtractionCommand(BaseInferenceCommand):
    """V2 CLI command for the generic all-purpose extraction utility.

    Owns the extraction-only flags (``--rag``, ``--raw-text``,
    ``--confidence``, ``--polygon``, ``--text-context``) and prepends the
    optional Raw Text / RAG sections to the ``full`` output.
    """

    name = "extraction"
    description = "Generic all-purpose extraction."

    def configure_product_options(self, parser: ArgumentParser) -> None:
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
        parser.add_argument(
            "-r",
            "--raw-text",
            dest="raw_text",
            action="store_true",
            help="Extract the full text content from the document.",
        )
        parser.add_argument(
            "-c",
            "--confidence",
            dest="confidence",
            action="store_true",
            help="Retrieve confidence scores for each field.",
        )
        parser.add_argument(
            "-p",
            "--polygon",
            dest="polygon",
            action="store_true",
            help="Retrieve bounding-box polygons for each field.",
        )
        parser.add_argument(
            "-t",
            "--text-context",
            dest="text_context",
            help="Additional text context used by the model during inference.",
            default=None,
        )

    def get_response_class(self) -> type:
        return ExtractionResponse

    def build_parameters(
        self,
        parsed_args: Namespace,
        model_id: str,
        alias: str | None,
    ) -> BaseParameters:
        return ExtractionParameters(
            model_id=model_id,
            alias=alias,
            rag=True if getattr(parsed_args, "rag", False) else None,
            raw_text=True if getattr(parsed_args, "raw_text", False) else None,
            polygon=True if getattr(parsed_args, "polygon", False) else None,
            confidence=(True if getattr(parsed_args, "confidence", False) else None),
            text_context=getattr(parsed_args, "text_context", None),
        )

    def get_full_output(self, parsed_args: Namespace, response) -> str:
        inference = getattr(response, "inference", None)
        if inference is None:
            return ""

        sections: list[str] = []
        active_options = getattr(inference, "active_options", None)
        result = getattr(inference, "result", None)

        if (
            getattr(parsed_args, "raw_text", False)
            and active_options is not None
            and getattr(active_options, "raw_text", False)
            and result is not None
            and getattr(result, "raw_text", None) is not None
        ):
            raw_text_str = str(result.raw_text).replace("\n", "\n  ")
            sections.append("#############\nRaw Text\n#############\n::")
            sections.append("  " + raw_text_str)
            sections.append("")

        if (
            getattr(parsed_args, "rag", False)
            and active_options is not None
            and getattr(active_options, "rag", False)
            and result is not None
            and getattr(result, "rag", None) is not None
        ):
            rag_str = str(result.rag).replace("\n", "\n  ")
            sections.append(
                "#############\nRetrieval-Augmented Generation\n#############\n::"
            )
            sections.append("  " + rag_str)
            sections.append("")

        sections.append(str(inference))
        return "\n".join(sections)
