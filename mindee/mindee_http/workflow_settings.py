from dataclasses import dataclass
from typing import Optional

from mindee.error.mindee_error import MindeeApiError
from mindee.mindee_http.base_settings import API_KEY_ENV_NAME, BaseSettings


@dataclass
class WorkflowSettings(BaseSettings):
    """Settings class relating to workflow requests."""

    def __init__(
        self,
        api_key: Optional[str],
        workflow_id: str,
    ):
        super().__init__(api_key)
        if not self.api_key or len(self.api_key) == 0:
            raise MindeeApiError(
                (
                    f"Missing API key for workflow '{workflow_id}',"
                    " check your Client configuration.\n"
                    "You can set this using the "
                    f"'{API_KEY_ENV_NAME}' environment variable."
                )
            )
        self.url_root = f"{self.base_url}/workflows/{workflow_id}/executions"
