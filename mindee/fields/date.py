from datetime import date, datetime
from typing import Optional

import pytz

from mindee.fields.base import BaseField, FieldPositionMixin, TypePrediction

ISO8601_DATE_FORMAT = "%Y-%m-%d"
ISO8601_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class DateField(FieldPositionMixin, BaseField):
    date_object: Optional[date] = None
    """Date as a standard Python ``datetime.date`` object."""
    value: Optional[str] = None
    """The raw field value."""

    def __init__(
        self,
        prediction: TypePrediction,
        reconstructed: bool = False,
        page_n: Optional[int] = None,
    ):
        """
        Date field object.

        :param prediction: Date prediction object from HTTP response
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_n: Page number for multi-page document
        """
        super().__init__(
            prediction,
            value_key="value",
            reconstructed=reconstructed,
            page_n=page_n,
        )
        self._set_position(prediction)

        if self.value:
            try:
                self.date_object = (
                    datetime.strptime(self.value, ISO8601_DATE_FORMAT)
                    .replace(tzinfo=pytz.utc)
                    .date()
                )
            except (TypeError, ValueError):
                self.date_object = None
                self.confidence = 0.0
