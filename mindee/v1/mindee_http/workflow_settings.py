from dataclasses import dataclass

from mindee.v1.error.mindee_api_error import MindeeAPIError
from mindee.v1.mindee_http.base_settings import API_KEY_ENV_NAME, BaseSettings


@dataclass
class WorkflowSettings(BaseSettings):
    """Settings class relating to workflow requests."""

    def __init__(
        self,
        api_key: str | None,
        workflow_id: str,
    ):
        super().__init__(api_key)
        if not self.api_key or len(self.api_key) == 0:
            raise MindeeAPIError(
                f"Missing API key for workflow '{workflow_id}',"
                " check your Client configuration.\n"
                "You can set this using the "
                f"'{API_KEY_ENV_NAME}' environment variable."
            )
        self.url_root = f"{self.base_url}/v1/workflows/{workflow_id}/executions"
