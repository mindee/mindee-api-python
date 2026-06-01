from typing import Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.v1.parsing.standard.classification import ClassificationField
from mindee.v1.product.fr.id_card.id_card_v1_document import (
    IdCardV1Document,
)


class IdCardV1Page(IdCardV1Document):
    """Carte Nationale d'Identité API version 1.1 page data."""

    document_side: ClassificationField
    """The side of the document which is visible."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Carte Nationale d'Identité page.

        :params raw_prediction: Raw prediction from HTTP response
        :params page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction=raw_prediction, page_id=page_id)
        self.document_side = ClassificationField(
            raw_prediction["document_side"],
            page_id=page_id,
        )

    def __str__(self) -> str:
        out_str: str = f":Document Side: {self.document_side}\n"
        out_str += f"{super().__str__()}"
        return clean_out_string(out_str)
