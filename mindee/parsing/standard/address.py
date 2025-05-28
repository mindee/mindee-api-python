from typing import Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.standard.text import StringField


class AddressField(StringField):
    """A field containing an address value."""

    street_number: Optional[str]
    """Street number."""
    street_name: Optional[str]
    """Street name."""
    po_box: Optional[str]
    """PO Box number."""
    address_complement: Optional[str]
    """Address complement."""
    city: Optional[str]
    """City name."""
    postal_code: Optional[str]
    """Postal code."""
    state: Optional[str]
    """State name."""
    country: Optional[str]
    """Country name."""

    def __init__(
        self,
        raw_prediction: StringDict,
        reconstructed: bool = False,
        page_id: Optional[int] = None,
    ):
        """
        Text field object.

        :param raw_prediction: Amount prediction object from HTTP response.
        :param reconstructed: Bool for reconstructed object (not extracted in the API).
        :param page_id: Page number for multi-page document.
        """
        self.value = None
        super().__init__(
            raw_prediction,
            value_key="value",
            reconstructed=reconstructed,
            page_id=page_id,
        )
        if raw_prediction.get("street_number"):
            self.street_number = raw_prediction["street_number"]
        if raw_prediction.get("street_name"):
            self.street_name = raw_prediction["street_name"]
        if raw_prediction.get("po_box"):
            self.po_box = raw_prediction["po_box"]
        if raw_prediction.get("address_complement"):
            self.address_complement = raw_prediction["address_complement"]
        if raw_prediction.get("city"):
            self.city = raw_prediction["city"]
        if raw_prediction.get("postal_code"):
            self.postal_code = raw_prediction["postal_code"]
        if raw_prediction.get("state"):
            self.city = raw_prediction["state"]
        if raw_prediction.get("country"):
            self.city = raw_prediction["country"]

    def __str__(self) -> str:
        return self.value if self.value else ""
