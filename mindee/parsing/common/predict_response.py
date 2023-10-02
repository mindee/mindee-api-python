from mindee.logger import logger
from mindee.parsing.common.api_response import ApiResponse, StringDict
from mindee.parsing.common.document import Document

class PredictResponse(ApiResponse):
    """
    Response of a prediction request.

    This is a generic class, so certain class properties depend on the document type.
    """
    document: Document
    # document: Optional[TypeDocument]
    # """An instance of the ``Document`` class, according to the type given."""

    def __init__(
        self,
        prediction_type,
        server_response: StringDict
    ) -> None:
        """
        Container for the raw API response and the parsed document.

        :param doc_config: DocumentConfig
        :param input_source: Input object
        :param http_response: json response from HTTP call
        """
        logger.debug("Handling API response")
        self.document = Document(prediction_type, server_response["document"])
