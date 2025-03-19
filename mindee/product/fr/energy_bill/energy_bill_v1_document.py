from typing import List, Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.amount import AmountField
from mindee.parsing.standard.date import DateField
from mindee.parsing.standard.text import StringField
from mindee.product.fr.energy_bill.energy_bill_v1_energy_consumer import (
    EnergyBillV1EnergyConsumer,
)
from mindee.product.fr.energy_bill.energy_bill_v1_energy_supplier import (
    EnergyBillV1EnergySupplier,
)
from mindee.product.fr.energy_bill.energy_bill_v1_energy_usage import (
    EnergyBillV1EnergyUsage,
)
from mindee.product.fr.energy_bill.energy_bill_v1_meter_detail import (
    EnergyBillV1MeterDetail,
)
from mindee.product.fr.energy_bill.energy_bill_v1_subscription import (
    EnergyBillV1Subscription,
)
from mindee.product.fr.energy_bill.energy_bill_v1_taxes_and_contribution import (
    EnergyBillV1TaxesAndContribution,
)


class EnergyBillV1Document(Prediction):
    """Energy Bill API version 1.2 document data."""

    contract_id: StringField
    """The unique identifier associated with a specific contract."""
    delivery_point: StringField
    """
    The unique identifier assigned to each electricity or gas consumption point. It specifies the exact
    location where the energy is delivered.
    """
    due_date: DateField
    """The date by which the payment for the energy invoice is due."""
    energy_consumer: EnergyBillV1EnergyConsumer
    """The entity that consumes the energy."""
    energy_supplier: EnergyBillV1EnergySupplier
    """The company that supplies the energy."""
    energy_usage: List[EnergyBillV1EnergyUsage]
    """Details of energy consumption."""
    invoice_date: DateField
    """The date when the energy invoice was issued."""
    invoice_number: StringField
    """The unique identifier of the energy invoice."""
    meter_details: EnergyBillV1MeterDetail
    """Information about the energy meter."""
    subscription: List[EnergyBillV1Subscription]
    """The subscription details fee for the energy service."""
    taxes_and_contributions: List[EnergyBillV1TaxesAndContribution]
    """Details of Taxes and Contributions."""
    total_amount: AmountField
    """The total amount to be paid for the energy invoice."""
    total_before_taxes: AmountField
    """The total amount to be paid for the energy invoice before taxes."""
    total_taxes: AmountField
    """Total of taxes applied to the invoice."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Energy Bill document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
        self.contract_id = StringField(
            raw_prediction["contract_id"],
            page_id=page_id,
        )
        self.delivery_point = StringField(
            raw_prediction["delivery_point"],
            page_id=page_id,
        )
        self.due_date = DateField(
            raw_prediction["due_date"],
            page_id=page_id,
        )
        self.energy_consumer = EnergyBillV1EnergyConsumer(
            raw_prediction["energy_consumer"],
            page_id=page_id,
        )
        self.energy_supplier = EnergyBillV1EnergySupplier(
            raw_prediction["energy_supplier"],
            page_id=page_id,
        )
        self.energy_usage = [
            EnergyBillV1EnergyUsage(prediction, page_id=page_id)
            for prediction in raw_prediction["energy_usage"]
        ]
        self.invoice_date = DateField(
            raw_prediction["invoice_date"],
            page_id=page_id,
        )
        self.invoice_number = StringField(
            raw_prediction["invoice_number"],
            page_id=page_id,
        )
        self.meter_details = EnergyBillV1MeterDetail(
            raw_prediction["meter_details"],
            page_id=page_id,
        )
        self.subscription = [
            EnergyBillV1Subscription(prediction, page_id=page_id)
            for prediction in raw_prediction["subscription"]
        ]
        self.taxes_and_contributions = [
            EnergyBillV1TaxesAndContribution(prediction, page_id=page_id)
            for prediction in raw_prediction["taxes_and_contributions"]
        ]
        self.total_amount = AmountField(
            raw_prediction["total_amount"],
            page_id=page_id,
        )
        self.total_before_taxes = AmountField(
            raw_prediction["total_before_taxes"],
            page_id=page_id,
        )
        self.total_taxes = AmountField(
            raw_prediction["total_taxes"],
            page_id=page_id,
        )

    @staticmethod
    def _subscription_separator(char: str) -> str:
        out_str = "  "
        out_str += f"+{char * 38}"
        out_str += f"+{char * 12}"
        out_str += f"+{char * 12}"
        out_str += f"+{char * 10}"
        out_str += f"+{char * 11}"
        out_str += f"+{char * 12}"
        return out_str + "+"

    def _subscription_to_str(self) -> str:
        if not self.subscription:
            return ""

        lines = f"\n{self._subscription_separator('-')}\n  ".join(
            [item.to_table_line() for item in self.subscription]
        )
        out_str = ""
        out_str += f"\n{self._subscription_separator('-')}\n "
        out_str += " | Description                         "
        out_str += " | End Date  "
        out_str += " | Start Date"
        out_str += " | Tax Rate"
        out_str += " | Total    "
        out_str += " | Unit Price"
        out_str += f" |\n{self._subscription_separator('=')}"
        out_str += f"\n  {lines}"
        out_str += f"\n{self._subscription_separator('-')}"
        return out_str

    @staticmethod
    def _energy_usage_separator(char: str) -> str:
        out_str = "  "
        out_str += f"+{char * 13}"
        out_str += f"+{char * 38}"
        out_str += f"+{char * 12}"
        out_str += f"+{char * 12}"
        out_str += f"+{char * 10}"
        out_str += f"+{char * 11}"
        out_str += f"+{char * 17}"
        out_str += f"+{char * 12}"
        return out_str + "+"

    def _energy_usage_to_str(self) -> str:
        if not self.energy_usage:
            return ""

        lines = f"\n{self._energy_usage_separator('-')}\n  ".join(
            [item.to_table_line() for item in self.energy_usage]
        )
        out_str = ""
        out_str += f"\n{self._energy_usage_separator('-')}\n "
        out_str += " | Consumption"
        out_str += " | Description                         "
        out_str += " | End Date  "
        out_str += " | Start Date"
        out_str += " | Tax Rate"
        out_str += " | Total    "
        out_str += " | Unit of Measure"
        out_str += " | Unit Price"
        out_str += f" |\n{self._energy_usage_separator('=')}"
        out_str += f"\n  {lines}"
        out_str += f"\n{self._energy_usage_separator('-')}"
        return out_str

    @staticmethod
    def _taxes_and_contributions_separator(char: str) -> str:
        out_str = "  "
        out_str += f"+{char * 38}"
        out_str += f"+{char * 12}"
        out_str += f"+{char * 12}"
        out_str += f"+{char * 10}"
        out_str += f"+{char * 11}"
        out_str += f"+{char * 12}"
        return out_str + "+"

    def _taxes_and_contributions_to_str(self) -> str:
        if not self.taxes_and_contributions:
            return ""

        lines = f"\n{self._taxes_and_contributions_separator('-')}\n  ".join(
            [item.to_table_line() for item in self.taxes_and_contributions]
        )
        out_str = ""
        out_str += f"\n{self._taxes_and_contributions_separator('-')}\n "
        out_str += " | Description                         "
        out_str += " | End Date  "
        out_str += " | Start Date"
        out_str += " | Tax Rate"
        out_str += " | Total    "
        out_str += " | Unit Price"
        out_str += f" |\n{self._taxes_and_contributions_separator('=')}"
        out_str += f"\n  {lines}"
        out_str += f"\n{self._taxes_and_contributions_separator('-')}"
        return out_str

    def __str__(self) -> str:
        out_str: str = f":Invoice Number: {self.invoice_number}\n"
        out_str += f":Contract ID: {self.contract_id}\n"
        out_str += f":Delivery Point: {self.delivery_point}\n"
        out_str += f":Invoice Date: {self.invoice_date}\n"
        out_str += f":Due Date: {self.due_date}\n"
        out_str += f":Total Before Taxes: {self.total_before_taxes}\n"
        out_str += f":Total Taxes: {self.total_taxes}\n"
        out_str += f":Total Amount: {self.total_amount}\n"
        out_str += f":Energy Supplier:\n{self.energy_supplier.to_field_list()}\n"
        out_str += f":Energy Consumer:\n{self.energy_consumer.to_field_list()}\n"
        out_str += f":Subscription: {self._subscription_to_str()}\n"
        out_str += f":Energy Usage: {self._energy_usage_to_str()}\n"
        out_str += (
            f":Taxes and Contributions: {self._taxes_and_contributions_to_str()}\n"
        )
        out_str += f":Meter Details:\n{self.meter_details.to_field_list()}\n"
        return clean_out_string(out_str)
