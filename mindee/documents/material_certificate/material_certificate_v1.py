from typing import Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.text import TextField


class MaterialCertificateV1(Document):
    """Material Certificate v1 prediction results."""

    certificate_type: TextField
    """Material Type field is the type of material used in the product, such as metal, plastic, or wood."""
    heat_number: TextField
    """Heat Number is a unique identifier assigned to a batch of material produced in a manufacturing process."""
    norm: TextField
    """Material Grade field is the designation of the material's chemical and physical properties."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        Material Certificate v1 prediction results.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type="material_certificate",
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
        self.certificate_type = TextField(
            api_prediction["certificate_type"],
            page_id=page_n,
        )
        self.heat_number = TextField(
            api_prediction["heat_number"],
            page_id=page_n,
        )
        self.norm = TextField(
            api_prediction["norm"],
            page_id=page_n,
        )

    def __str__(self) -> str:
        return clean_out_string(
            "Material Certificate V1 Prediction\n"
            "==================================\n"
            f":Filename: {self.filename or ''}\n"
            f":Material Type: {self.certificate_type}\n"
            f":Material Grade: {self.norm}\n"
            f":Heat Number: {self.heat_number}\n"
        )


TypeMaterialCertificateV1 = TypeVar(
    "TypeMaterialCertificateV1", bound=MaterialCertificateV1
)
