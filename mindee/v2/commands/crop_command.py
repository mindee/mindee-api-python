from argparse import Namespace

from mindee import CropParameters, CropResponse
from mindee.v2.client_options.base_parameters import BaseParameters
from mindee.v2.commands.base_inference_command import BaseInferenceCommand


class CropCommand(BaseInferenceCommand):
    """V2 CLI command for the crop utility."""

    name = "crop"
    description = "Crop utility."

    def get_response_class(self) -> type:
        return CropResponse

    def build_parameters(
        self,
        parsed_args: Namespace,
        model_id: str,
        alias: str | None,
    ) -> BaseParameters:
        del parsed_args
        return CropParameters(model_id=model_id, alias=alias)
