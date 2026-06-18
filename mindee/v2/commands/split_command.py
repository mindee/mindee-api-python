from argparse import Namespace

from mindee import SplitParameters, SplitResponse
from mindee.v2.client_options.base_parameters import BaseParameters
from mindee.v2.commands.base_inference_command import BaseInferenceCommand


class SplitCommand(BaseInferenceCommand):
    """V2 CLI command for the split utility."""

    name = "split"
    description = "Split utility."

    def get_response_class(self) -> type:
        return SplitResponse

    def build_parameters(
        self,
        parsed_args: Namespace,
        model_id: str,
        alias: str | None,
    ) -> BaseParameters:
        del parsed_args
        return SplitParameters(model_id=model_id, alias=alias)
