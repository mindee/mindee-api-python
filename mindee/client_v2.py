from time import sleep
from typing import Optional, Union

from mindee.client_mixin import ClientMixin
from mindee.error.mindee_error import MindeeError
from mindee.error.mindee_http_error_v2 import handle_error_v2
from mindee.input.inference_predict_options import InferencePredictOptions
from mindee.input.local_response import LocalResponse
from mindee.input.polling_options import PollingOptions
from mindee.input.sources.local_input_source import LocalInputSource
from mindee.logger import logger
from mindee.mindee_http.mindee_api_v2 import MindeeApiV2
from mindee.mindee_http.response_validation_v2 import (
    is_valid_get_response,
    is_valid_post_response,
)
from mindee.parsing.v2.inference_response import InferenceResponse
from mindee.parsing.v2.polling_response import PollingResponse


class ClientV2(ClientMixin):
    """
    Mindee API Client.

    See: https://developers.mindee.com/docs/
    """

    api_key: Optional[str]
    mindee_api: MindeeApiV2

    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        Mindee API Client.

        :param api_key: Your API key for all endpoints
        """
        self.api_key = api_key
        self.mindee_api = MindeeApiV2(api_key)

    def enqueue(
        self, input_source: LocalInputSource, options: InferencePredictOptions
    ) -> PollingResponse:
        """
        Enqueues a document to a given model.

        :param input_source: The document/source file to use.
            Has to be created beforehand.

        :param options: Options for the prediction.
        :return: A valid inference response.
        """
        logger.debug("Enqueuing document to '%s'", options.model_id)

        if options.page_options and input_source.is_pdf():
            input_source.process_pdf(
                options.page_options.operation,
                options.page_options.on_min_pages,
                options.page_options.page_indexes,
            )

        response = self.mindee_api.predict_async_req_post(
            input_source=input_source, options=options
        )
        dict_response = response.json()

        if not is_valid_post_response(response):
            handle_error_v2(dict_response)

        return PollingResponse(dict_response)

    def parse_queued(
        self,
        queue_id: str,
    ) -> Union[InferenceResponse, PollingResponse]:
        """
        Parses a queued document.

        :param queue_id: queue_id received from the API.
        """
        logger.debug("Fetching from queue '%s'.", queue_id)

        response = self.mindee_api.get_inference_from_queue(queue_id)
        if not is_valid_get_response(response):
            handle_error_v2(response.json())

        dict_response = response.json()
        if "job" in dict_response:
            return PollingResponse(dict_response)
        return InferenceResponse(dict_response)

    def enqueue_and_parse(
        self, input_source: LocalInputSource, options: InferencePredictOptions
    ) -> InferenceResponse:
        """
        Enqueues to an asynchronous endpoint and automatically polls for a response.

        :param input_source: The document/source file to use.
            Has to be created beforehand.

        :param options: Options for the prediction.

        :return: A valid inference response.
        """
        if not options.polling_options:
            options.polling_options = PollingOptions()
        self._validate_async_params(
            options.polling_options.initial_delay_sec,
            options.polling_options.delay_sec,
            options.polling_options.max_retries,
        )
        queue_result = self.enqueue(input_source, options)
        logger.debug(
            "Successfully enqueued document with job id: %s", queue_result.job.id
        )
        sleep(options.polling_options.initial_delay_sec)
        retry_counter = 1
        poll_results = self.parse_queued(
            queue_result.job.id,
        )
        while retry_counter < options.polling_options.max_retries:
            if not isinstance(poll_results, PollingResponse):
                break
            if poll_results.job.status == "Failed":
                raise MindeeError(f"Parsing failed for job {poll_results.job.id}")
            logger.debug(
                "Polling server for parsing result with job id: %s",
                queue_result.job.id,
            )
            retry_counter += 1
            sleep(options.polling_options.delay_sec)
            poll_results = self.parse_queued(queue_result.job.id)

        if not isinstance(poll_results, InferenceResponse):
            raise MindeeError(
                f"Couldn't retrieve document after {retry_counter} tries."
            )

        return poll_results

    @staticmethod
    def load_inference(local_response: LocalResponse) -> InferenceResponse:
        """
        Load a prediction from the V2 API.

        :param local_response: Local response to load.
        :return: A valid prediction.
        """
        try:
            return InferenceResponse(local_response.as_dict)
        except KeyError as exc:
            raise MindeeError("No prediction found in local response.") from exc
