import httpx

from mindee.input.local_input_source import LocalInputSource
from mindee.input.url_input_source import URLInputSource
from mindee.parsing.common.string_dict import StringDict
from mindee.v1.client_options.workflow_options import WorkflowOptions
from mindee.v1.mindee_http.base_endpoint import BaseEndpoint
from mindee.v1.mindee_http.workflow_settings import WorkflowSettings


class WorkflowEndpoint(BaseEndpoint):
    """Workflow endpoint."""

    settings: WorkflowSettings
    """Settings object."""

    def __init__(
        self, settings: WorkflowSettings, http_client: httpx.Client | None = None
    ) -> None:
        """
        Workflow Endpoint.

        :param settings: Settings object.
        """
        super().__init__(settings, http_client)

    def workflow_execution_post(
        self,
        input_source: LocalInputSource | URLInputSource,
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
        post_kwargs: StringDict = {
            "headers": self.settings.base_headers,
            "params": params,
            "timeout": self.settings.request_timeout,
        }

        if isinstance(input_source, URLInputSource):
            data["document"] = input_source.url
        else:
            post_kwargs["files"] = {"document": input_source.read_contents(True)}
        post_kwargs["data"] = data
        if self.http_client is None or self.http_client.is_closed:
            return httpx.post(self.settings.url_root, **post_kwargs)
        return self.http_client.post(self.settings.url_root, **post_kwargs)
