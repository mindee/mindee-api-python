from typing import List, Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.date import DateField
from mindee.parsing.standard.text import StringField
from mindee.product.bill_of_lading.bill_of_lading_v1_carrier import (
    BillOfLadingV1Carrier,
)
from mindee.product.bill_of_lading.bill_of_lading_v1_carrier_item import (
    BillOfLadingV1CarrierItem,
)
from mindee.product.bill_of_lading.bill_of_lading_v1_consignee import (
    BillOfLadingV1Consignee,
)
from mindee.product.bill_of_lading.bill_of_lading_v1_notify_party import (
    BillOfLadingV1NotifyParty,
)
from mindee.product.bill_of_lading.bill_of_lading_v1_shipper import (
    BillOfLadingV1Shipper,
)


class BillOfLadingV1Document(Prediction):
    """Bill of Lading API version 1.1 document data."""

    bill_of_lading_number: StringField
    """A unique identifier assigned to a Bill of Lading document."""
    carrier: BillOfLadingV1Carrier
    """The shipping company responsible for transporting the goods."""
    carrier_items: List[BillOfLadingV1CarrierItem]
    """The goods being shipped."""
    consignee: BillOfLadingV1Consignee
    """The party to whom the goods are being shipped."""
    date_of_issue: DateField
    """The date when the bill of lading is issued."""
    departure_date: DateField
    """The date when the vessel departs from the port of loading."""
    notify_party: BillOfLadingV1NotifyParty
    """The party to be notified of the arrival of the goods."""
    place_of_delivery: StringField
    """The place where the goods are to be delivered."""
    port_of_discharge: StringField
    """The port where the goods are unloaded from the vessel."""
    port_of_loading: StringField
    """The port where the goods are loaded onto the vessel."""
    shipper: BillOfLadingV1Shipper
    """The party responsible for shipping the goods."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Bill of Lading document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
        self.bill_of_lading_number = StringField(
            raw_prediction["bill_of_lading_number"],
            page_id=page_id,
        )
        self.carrier = BillOfLadingV1Carrier(
            raw_prediction["carrier"],
            page_id=page_id,
        )
        self.carrier_items = [
            BillOfLadingV1CarrierItem(prediction, page_id=page_id)
            for prediction in raw_prediction["carrier_items"]
        ]
        self.consignee = BillOfLadingV1Consignee(
            raw_prediction["consignee"],
            page_id=page_id,
        )
        self.date_of_issue = DateField(
            raw_prediction["date_of_issue"],
            page_id=page_id,
        )
        self.departure_date = DateField(
            raw_prediction["departure_date"],
            page_id=page_id,
        )
        self.notify_party = BillOfLadingV1NotifyParty(
            raw_prediction["notify_party"],
            page_id=page_id,
        )
        self.place_of_delivery = StringField(
            raw_prediction["place_of_delivery"],
            page_id=page_id,
        )
        self.port_of_discharge = StringField(
            raw_prediction["port_of_discharge"],
            page_id=page_id,
        )
        self.port_of_loading = StringField(
            raw_prediction["port_of_loading"],
            page_id=page_id,
        )
        self.shipper = BillOfLadingV1Shipper(
            raw_prediction["shipper"],
            page_id=page_id,
        )

    @staticmethod
    def _carrier_items_separator(char: str) -> str:
        out_str = "  "
        out_str += f"+{char * 38}"
        out_str += f"+{char * 14}"
        out_str += f"+{char * 13}"
        out_str += f"+{char * 18}"
        out_str += f"+{char * 10}"
        out_str += f"+{char * 13}"
        return out_str + "+"

    def _carrier_items_to_str(self) -> str:
        if not self.carrier_items:
            return ""

        lines = f"\n{self._carrier_items_separator('-')}\n  ".join(
            [item.to_table_line() for item in self.carrier_items]
        )
        out_str = ""
        out_str += f"\n{self._carrier_items_separator('-')}\n "
        out_str += " | Description                         "
        out_str += " | Gross Weight"
        out_str += " | Measurement"
        out_str += " | Measurement Unit"
        out_str += " | Quantity"
        out_str += " | Weight Unit"
        out_str += f" |\n{self._carrier_items_separator('=')}"
        out_str += f"\n  {lines}"
        out_str += f"\n{self._carrier_items_separator('-')}"
        return out_str

    def __str__(self) -> str:
        out_str: str = f":Bill of Lading Number: {self.bill_of_lading_number}\n"
        out_str += f":Shipper:\n{self.shipper.to_field_list()}\n"
        out_str += f":Consignee:\n{self.consignee.to_field_list()}\n"
        out_str += f":Notify Party:\n{self.notify_party.to_field_list()}\n"
        out_str += f":Carrier:\n{self.carrier.to_field_list()}\n"
        out_str += f":Items: {self._carrier_items_to_str()}\n"
        out_str += f":Port of Loading: {self.port_of_loading}\n"
        out_str += f":Port of Discharge: {self.port_of_discharge}\n"
        out_str += f":Place of Delivery: {self.place_of_delivery}\n"
        out_str += f":Date of issue: {self.date_of_issue}\n"
        out_str += f":Departure Date: {self.departure_date}\n"
        return clean_out_string(out_str)
