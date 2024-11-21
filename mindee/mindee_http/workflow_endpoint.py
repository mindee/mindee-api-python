from typing import Optional, Union

import requests

from mindee.input import LocalInputSource, UrlInputSource
from mindee.mindee_http import BaseEndpoint
from mindee.mindee_http.workflow_settings import WorkflowSettings
from mindee.parsing.common.execution_priority import ExecutionPriority


class WorkflowEndpoint(BaseEndpoint):
    """Workflow endpoint."""

    settings: WorkflowSettings

    def __init__(self, settings: WorkflowSettings) -> None:
        """
        Workflow Endpoint.

        :param settings: Settings object.
        """
        super().__init__(settings)

    def workflow_execution_post(
        self,
        input_source: Union[LocalInputSource, UrlInputSource],
        alias: Optional[str] = None,
        priority: Optional[ExecutionPriority] = None,
        full_text: bool = False,
    ):
        """
        Sends the document to the workflow.

        :param input_source: The document/source file to use.
            Has to be created beforehand.
        :param alias: Optional alias for the document.
        :param priority: Priority for the document.
        :param full_text: Whether to include the full OCR text response in compatible APIs.
        :return:
        """
        data = {}

        if alias:
            data["alias"] = alias
        if priority:
            data["priority"] = priority.value

        params = {}
        if full_text:
            params["full_text_ocr"] = "true"

        if isinstance(input_source, UrlInputSource):
            data["document"] = input_source.url
            response = requests.post(
                self.settings.url_root,
                headers=self.settings.base_headers,
                data=data,
                params=params,
                timeout=self.settings.request_timeout,
            )
        else:
            files = {"document": input_source.read_contents(True)}
            response = requests.post(
                self.settings.url_root,
                files=files,
                headers=self.settings.base_headers,
                data=data,
                params=params,
                timeout=self.settings.request_timeout,
            )

        return response
