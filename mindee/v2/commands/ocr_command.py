from argparse import Namespace

from mindee import OCRParameters, OCRResponse
from mindee.v2.client_options.base_parameters import BaseParameters
from mindee.v2.commands.base_inference_command import BaseInferenceCommand


class OcrCommand(BaseInferenceCommand):
    """V2 CLI command for the OCR utility."""

    name = "ocr"
    description = "OCR utility."

    def get_response_class(self) -> type:
        return OCRResponse

    def build_parameters(
        self,
        parsed_args: Namespace,
        model_id: str,
        alias: str | None,
    ) -> BaseParameters:
        del parsed_args
        return OCRParameters(model_id=model_id, alias=alias)
