from argparse import Namespace

from mindee import ClassificationParameters, ClassificationResponse
from mindee.v2.client_options.base_parameters import BaseParameters
from mindee.v2.commands.base_inference_command import BaseInferenceCommand


class ClassificationCommand(BaseInferenceCommand):
    """V2 CLI command for the classification utility."""

    name = "classification"
    description = "Classification utility."

    def get_response_class(self) -> type:
        return ClassificationResponse

    def build_parameters(
        self,
        parsed_args: Namespace,
        model_id: str,
        alias: str | None,
    ) -> BaseParameters:
        del parsed_args
        return ClassificationParameters(model_id=model_id, alias=alias)
