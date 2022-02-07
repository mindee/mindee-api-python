from typing import Optional
from datetime import datetime, date
import pytz
from mindee.fields.base import Field

ISO8601_DATE_FORMAT = "%Y-%m-%d"
ISO8601_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class Date(Field):
    date_object: Optional[date]

    def __init__(
        self, date_prediction, value_key="iso", reconstructed=False, page_n=None
    ):
        """
        :param date_prediction: Date prediction object from HTTP response
        :param value_key: Key to use in the date_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_n: Page number for multi pages pdf
        """
        super().__init__(
            date_prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_n=page_n,
        )

        try:
            self.date_object = (
                datetime.strptime(self.value, ISO8601_DATE_FORMAT)
                .replace(tzinfo=pytz.utc)
                .date()
            )
        except (TypeError, ValueError):
            self.date_object = None
            self.confidence = 0.0
            self.value = None
            self.bbox = []
