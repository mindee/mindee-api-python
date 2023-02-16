from typing import Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.text import TextField


class ShippingContainerV1(Document):
    """Shipping Container v1 prediction results."""

    owner: TextField
    """The ISO-6346 code for container owner and equipment identifier."""
    serial_number: TextField
    """ISO-6346 code for container serial number."""
    size_type: TextField
    """ISO 6346 code for container length, height and type."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        Shipping Container v1 prediction results.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type="shipping_container",
            api_prediction=api_prediction,
            page_n=page_n,
        )
        self._build_from_api_prediction(api_prediction["prediction"], page_n=page_n)

    def _build_from_api_prediction(
        self, api_prediction: TypeApiPrediction, page_n: Optional[int] = None
    ) -> None:
        """
        Build the object from the prediction API JSON.

        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number
        """
        self.owner = TextField(
            api_prediction["owner"],
            page_n=page_n,
        )
        self.serial_number = TextField(
            api_prediction["serial_number"],
            page_n=page_n,
        )
        self.size_type = TextField(
            api_prediction["size_type"],
            page_n=page_n,
        )

    def __str__(self) -> str:
        return clean_out_string(
            "----- Shipping Container V1 -----\n"
            f"Filename: {self.filename or ''}\n"
            f"Owner: { self.owner }\n"
            f"Serial Number: { self.serial_number }\n"
            f"Size and Type: { self.size_type }\n"
            "----------------------"
        )


TypeShippingContainerV1 = TypeVar("TypeShippingContainerV1", bound=ShippingContainerV1)
