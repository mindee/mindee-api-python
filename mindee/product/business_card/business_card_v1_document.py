from typing import List, Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.text import StringField


class BusinessCardV1Document(Prediction):
    """Business Card API version 1.0 document data."""

    address: StringField
    """The address of the person."""
    company: StringField
    """The company the person works for."""
    email: StringField
    """The email address of the person."""
    fax_number: StringField
    """The Fax number of the person."""
    firstname: StringField
    """The given name of the person."""
    job_title: StringField
    """The job title of the person."""
    lastname: StringField
    """The lastname of the person."""
    mobile_number: StringField
    """The mobile number of the person."""
    phone_number: StringField
    """The phone number of the person."""
    social_media: List[StringField]
    """The social media profiles of the person or company."""
    website: StringField
    """The website of the person or company."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Business Card document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
        self.address = StringField(
            raw_prediction["address"],
            page_id=page_id,
        )
        self.company = StringField(
            raw_prediction["company"],
            page_id=page_id,
        )
        self.email = StringField(
            raw_prediction["email"],
            page_id=page_id,
        )
        self.fax_number = StringField(
            raw_prediction["fax_number"],
            page_id=page_id,
        )
        self.firstname = StringField(
            raw_prediction["firstname"],
            page_id=page_id,
        )
        self.job_title = StringField(
            raw_prediction["job_title"],
            page_id=page_id,
        )
        self.lastname = StringField(
            raw_prediction["lastname"],
            page_id=page_id,
        )
        self.mobile_number = StringField(
            raw_prediction["mobile_number"],
            page_id=page_id,
        )
        self.phone_number = StringField(
            raw_prediction["phone_number"],
            page_id=page_id,
        )
        self.social_media = [
            StringField(prediction, page_id=page_id)
            for prediction in raw_prediction["social_media"]
        ]
        self.website = StringField(
            raw_prediction["website"],
            page_id=page_id,
        )

    def __str__(self) -> str:
        social_media = f"\n { ' ' * 14 }".join(
            [str(item) for item in self.social_media],
        )
        out_str: str = f":Firstname: {self.firstname}\n"
        out_str += f":Lastname: {self.lastname}\n"
        out_str += f":Job Title: {self.job_title}\n"
        out_str += f":Company: {self.company}\n"
        out_str += f":Email: {self.email}\n"
        out_str += f":Phone Number: {self.phone_number}\n"
        out_str += f":Mobile Number: {self.mobile_number}\n"
        out_str += f":Fax Number: {self.fax_number}\n"
        out_str += f":Address: {self.address}\n"
        out_str += f":Website: {self.website}\n"
        out_str += f":Social Media: {social_media}\n"
        return clean_out_string(out_str)
