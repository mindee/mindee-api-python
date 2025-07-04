from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.common_response import CommonResponse
from mindee.parsing.v2.job import Job


class PollingResponse(CommonResponse):
    """Represent an inference response from Mindee V2 API."""

    job: Job
    """Job for the polling."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.job = Job(raw_response["job"])
