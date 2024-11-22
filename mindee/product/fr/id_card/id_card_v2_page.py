from typing import Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.classification import ClassificationField
from mindee.product.fr.id_card.id_card_v2_document import (
    IdCardV2Document,
)


class IdCardV2Page(IdCardV2Document):
    """Carte Nationale d'Identité API version 2.0 page data."""

    document_side: ClassificationField
    """The sides of the document which are visible."""
    document_type: ClassificationField
    """The document type or format."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Carte Nationale d'Identité page.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction=raw_prediction, page_id=page_id)
        self.document_side = ClassificationField(
            raw_prediction["document_side"],
            page_id=page_id,
        )
        self.document_type = ClassificationField(
            raw_prediction["document_type"],
            page_id=page_id,
        )

    def __str__(self) -> str:
        out_str: str = f":Document Type: {self.document_type}\n"
        out_str += f":Document Sides: {self.document_side}\n"
        out_str += f"{super().__str__()}"
        return clean_out_string(out_str)
