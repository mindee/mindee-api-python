from typing import Optional

from mindee.parsing.common import StringDict, clean_out_string
from mindee.product.fr.id_card.id_card_v2_document import IdCardV2Document

from mindee.parsing.standard import ClassificationField


class IdCardV2Page(IdCardV2Document):
    """Page data for Carte Nationale d'Identité, API version 2."""

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
        return clean_out_string(
            f":Document Type: {self.document_type}\n" f":Document Sides: {self.document_side}\n" + f"{super().__str__()}"
        )
