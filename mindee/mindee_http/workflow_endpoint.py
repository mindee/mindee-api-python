from typing import Union

import requests

from mindee.input import LocalInputSource, UrlInputSource, WorkflowOptions
from mindee.mindee_http.base_endpoint import BaseEndpoint
from mindee.mindee_http.workflow_settings import WorkflowSettings


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
        options: WorkflowOptions,
    ):
        """
        Sends the document to the workflow.

        :param input_source: The document/source file to use.
            Has to be created beforehand.
        :param options: Options for the workflow.
        :return:
        """
        data = {}

        if options.alias:
            data["alias"] = options.alias
        if options.priority:
            data["priority"] = options.priority.value
        if options.public_url:
            data["public_url"] = options.public_url

        params = {}
        if options.full_text:
            params["full_text_ocr"] = "true"
        if options.rag:
            params["rag"] = "true"

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
