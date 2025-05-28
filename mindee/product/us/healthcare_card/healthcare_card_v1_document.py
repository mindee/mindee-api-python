from typing import List, Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.date import DateField
from mindee.parsing.standard.text import StringField
from mindee.product.us.healthcare_card.healthcare_card_v1_copay import (
    HealthcareCardV1Copay,
)


class HealthcareCardV1Document(Prediction):
    """Healthcare Card API version 1.3 document data."""

    company_name: StringField
    """The name of the company that provides the healthcare plan."""
    copays: List[HealthcareCardV1Copay]
    """Copayments for covered services."""
    dependents: List[StringField]
    """The list of dependents covered by the healthcare plan."""
    enrollment_date: DateField
    """The date when the member enrolled in the healthcare plan."""
    group_number: StringField
    """The group number associated with the healthcare plan."""
    issuer_80840: StringField
    """The organization that issued the healthcare plan."""
    member_id: StringField
    """The unique identifier for the member in the healthcare system."""
    member_name: StringField
    """The name of the member covered by the healthcare plan."""
    payer_id: StringField
    """The unique identifier for the payer in the healthcare system."""
    plan_name: StringField
    """The name of the healthcare plan."""
    rx_bin: StringField
    """The BIN number for prescription drug coverage."""
    rx_grp: StringField
    """The group number for prescription drug coverage."""
    rx_id: StringField
    """The ID number for prescription drug coverage."""
    rx_pcn: StringField
    """The PCN number for prescription drug coverage."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Healthcare Card document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
        self.company_name = StringField(
            raw_prediction["company_name"],
            page_id=page_id,
        )
        self.copays = [
            HealthcareCardV1Copay(prediction, page_id=page_id)
            for prediction in raw_prediction["copays"]
        ]
        self.dependents = [
            StringField(prediction, page_id=page_id)
            for prediction in raw_prediction["dependents"]
        ]
        self.enrollment_date = DateField(
            raw_prediction["enrollment_date"],
            page_id=page_id,
        )
        self.group_number = StringField(
            raw_prediction["group_number"],
            page_id=page_id,
        )
        self.issuer_80840 = StringField(
            raw_prediction["issuer_80840"],
            page_id=page_id,
        )
        self.member_id = StringField(
            raw_prediction["member_id"],
            page_id=page_id,
        )
        self.member_name = StringField(
            raw_prediction["member_name"],
            page_id=page_id,
        )
        self.payer_id = StringField(
            raw_prediction["payer_id"],
            page_id=page_id,
        )
        self.plan_name = StringField(
            raw_prediction["plan_name"],
            page_id=page_id,
        )
        self.rx_bin = StringField(
            raw_prediction["rx_bin"],
            page_id=page_id,
        )
        self.rx_grp = StringField(
            raw_prediction["rx_grp"],
            page_id=page_id,
        )
        self.rx_id = StringField(
            raw_prediction["rx_id"],
            page_id=page_id,
        )
        self.rx_pcn = StringField(
            raw_prediction["rx_pcn"],
            page_id=page_id,
        )

    @staticmethod
    def _copays_separator(char: str) -> str:
        out_str = "  "
        out_str += f"+{char * 14}"
        out_str += f"+{char * 22}"
        return out_str + "+"

    def _copays_to_str(self) -> str:
        if not self.copays:
            return ""

        lines = f"\n{self._copays_separator('-')}\n  ".join(
            [item.to_table_line() for item in self.copays]
        )
        out_str = ""
        out_str += f"\n{self._copays_separator('-')}\n "
        out_str += " | Service Fees"
        out_str += " | Service Name        "
        out_str += f" |\n{self._copays_separator('=')}"
        out_str += f"\n  {lines}"
        out_str += f"\n{self._copays_separator('-')}"
        return out_str

    def __str__(self) -> str:
        dependents = f"\n { ' ' * 12 }".join(
            [str(item) for item in self.dependents],
        )
        out_str: str = f":Company Name: {self.company_name}\n"
        out_str += f":Plan Name: {self.plan_name}\n"
        out_str += f":Member Name: {self.member_name}\n"
        out_str += f":Member ID: {self.member_id}\n"
        out_str += f":Issuer 80840: {self.issuer_80840}\n"
        out_str += f":Dependents: {dependents}\n"
        out_str += f":Group Number: {self.group_number}\n"
        out_str += f":Payer ID: {self.payer_id}\n"
        out_str += f":RX BIN: {self.rx_bin}\n"
        out_str += f":RX ID: {self.rx_id}\n"
        out_str += f":RX GRP: {self.rx_grp}\n"
        out_str += f":RX PCN: {self.rx_pcn}\n"
        out_str += f":Copays: {self._copays_to_str()}\n"
        out_str += f":Enrollment Date: {self.enrollment_date}\n"
        return clean_out_string(out_str)
