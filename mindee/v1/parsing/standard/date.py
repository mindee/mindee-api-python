from datetime import date, datetime

from mindee.parsing.common.string_dict import StringDict
from mindee.v1.parsing.standard.base import BaseField, FieldPositionMixin

ISO8601_DATE_FORMAT = "%Y-%m-%d"
ISO8601_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class DateField(FieldPositionMixin, BaseField):
    """A field containing a date value."""

    date_object: date | None
    """Date as a standard Python ``datetime.date`` object."""
    value: str | None
    """The raw field value."""
    is_computed: bool | None
    """Whether the field was computed or retrieved directly from the document."""

    def __init__(
        self,
        raw_prediction: StringDict,
        reconstructed: bool = False,
        page_id: int | None = None,
    ):
        """
        Date field object.

        :param raw_prediction: Date prediction object from HTTP response
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_id: Page number for multi-page document
        """
        super().__init__(
            raw_prediction,
            value_key="value",
            reconstructed=reconstructed,
            page_id=page_id,
        )
        self._set_position(raw_prediction)

        if "is_computed" in raw_prediction:
            self.is_computed = raw_prediction["is_computed"]
        if self.value:
            try:
                self.date_object = datetime.strptime(
                    self.value, ISO8601_DATE_FORMAT
                ).date()
            except (TypeError, ValueError):
                self.date_object = None
                self.confidence = 0.0
        else:
            self.date_object = None
            self.confidence = 0.0
            self.value = None
