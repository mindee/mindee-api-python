from datetime import datetime
from typing import List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.base import field_array_confidence
from mindee.fields.date import DateField
from mindee.fields.text import TextField


class PassportV1(Document):
    """Passport v1 prediction results."""

    birth_date: DateField
    """The date of birth of the passport holder."""
    birth_place: TextField
    """The place of birth of the passport holder."""
    country: TextField
    """The country's 3 letter code (ISO 3166-1 alpha-3)."""
    expiry_date: DateField
    """The expiry date of the passport."""
    full_name: TextField
    """
    Holder's full name.
    The combination of `given_names` and `surname` fields.
    """
    gender: TextField
    """The gender of the passport holder."""
    given_names: List[TextField]
    """The given name(s) of the passport holder."""
    id_number: TextField
    """The passport's identification number."""
    issuance_date: DateField
    """The date the passport was issued."""
    mrz: TextField
    """Combination of both MRZ fields."""
    mrz1: TextField
    """Machine Readable Zone, first line"""
    mrz2: TextField
    """Machine Readable Zone, second line"""
    surname: TextField
    """The surname of the passport holder."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        Passport v1 prediction results.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type="passport",
            api_prediction=api_prediction,
            page_n=page_n,
        )
        self._build_from_api_prediction(api_prediction["prediction"], page_n=page_n)
        self._checklist()
        self._reconstruct()

    def _build_from_api_prediction(
        self, api_prediction: TypeApiPrediction, page_n: Optional[int] = None
    ) -> None:
        """
        Build the object from the prediction API JSON.

        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number for multi pages pdf input
        """
        self.birth_date = DateField(
            api_prediction["birth_date"],
            page_id=page_n,
        )
        self.birth_place = TextField(
            api_prediction["birth_place"],
            page_id=page_n,
        )
        self.country = TextField(
            api_prediction["country"],
            page_id=page_n,
        )
        self.expiry_date = DateField(
            api_prediction["expiry_date"],
            page_id=page_n,
        )
        self.gender = TextField(
            api_prediction["gender"],
            page_id=page_n,
        )
        self.given_names = [
            TextField(prediction, page_id=page_n)
            for prediction in api_prediction["given_names"]
        ]
        self.id_number = TextField(
            api_prediction["id_number"],
            page_id=page_n,
        )
        self.issuance_date = DateField(
            api_prediction["issuance_date"],
            page_id=page_n,
        )
        self.mrz1 = TextField(
            api_prediction["mrz1"],
            page_id=page_n,
        )
        self.mrz2 = TextField(
            api_prediction["mrz2"],
            page_id=page_n,
        )
        self.surname = TextField(
            api_prediction["surname"],
            page_id=page_n,
        )
        self.mrz = TextField({"value": None, "confidence": 0.0}, page_id=page_n)
        self.full_name = TextField({"value": None, "confidence": 0.0}, page_id=page_n)

    def __str__(self) -> str:
        given_names = f"\n { ' ' * 15 }".join(
            [str(item) for item in self.given_names],
        )
        return clean_out_string(
            "Passport V1 Prediction\n"
            "======================\n"
            f":Filename: {self.filename or ''}\n"
            f":Country Code: {self.country}\n"
            f":ID Number: {self.id_number}\n"
            f":Given Name(s): {given_names}\n"
            f":Surname: {self.surname}\n"
            f":Date of Birth: {self.birth_date}\n"
            f":Place of Birth: {self.birth_place}\n"
            f":Gender: {self.gender}\n"
            f":Date of Issue: {self.issuance_date}\n"
            f":Expiry Date: {self.expiry_date}\n"
            f":MRZ Line 1: {self.mrz1}\n"
            f":MRZ Line 2: {self.mrz2}\n"
        )

    def is_expired(self) -> bool:
        """
        Check the passport's validity.

        :return: True if the passport is expired, False otherwise
        """
        if not self.expiry_date.date_object:
            return True
        return self.expiry_date.date_object < datetime.date(datetime.now())

    @staticmethod
    def check_sum(to_check: str) -> str:
        """
        Validate the checksum.

        https://en.wikipedia.org/wiki/Machine-readable_passport

        :param to_check: MRZ value to check
        :return: checksum of the value
        """
        checker = 0
        alpha_to_num = {c: 10 + i for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
        for i, chk in enumerate(to_check):
            if i % 3 == 0:
                weight = 7
            elif i % 3 == 1:
                weight = 3
            else:
                weight = 1

            if chk == "<":
                val = 0
            elif chk.isalpha():
                val = alpha_to_num[chk]
            else:
                val = int(chk)
            checker += val * weight
        return str(checker % 10)

    def _reconstruct(self) -> None:
        """Call fields reconstruction methods."""
        self.__reconstruct_mrz()
        self.__reconstruct_full_name()

    def _checklist(self) -> None:
        """Call check methods."""
        self.checklist = {
            "mrz_id_number_checksum": self.__mrz_id_number_checksum(),
            "mrz_date_of_birth_checksum": self.__mrz_date_of_birth_checksum(),
            "mrz_expiration_date_checksum": self.__mrz_expiration_date_checksum(),
            "mrz_personal_number_checksum": self.__mrz_personal_number_checksum(),
            "mrz_last_name_checksum": self.__mrz_last_name_checksum(),
        }

    # Checks

    def __mrz_id_number_checksum(self) -> bool:
        """
        Validate the ID number's MRZ checksum.

        :return: True if valid, False otherwise
        """
        if self.mrz2.value is None:
            return False
        if PassportV1.check_sum(self.mrz2.value[:9]) == self.mrz2.value[9]:
            self.id_number.confidence = 1.0
            return True
        return False

    def __mrz_date_of_birth_checksum(self) -> bool:
        """
        Validate the date of birth's MRZ checksum.

        :return: True if valid, False otherwise
        """
        if self.mrz2.value is None:
            return False
        if PassportV1.check_sum(self.mrz2.value[13:19]) == self.mrz2.value[19]:
            self.birth_date.confidence = 1.0
            return True
        return False

    def __mrz_expiration_date_checksum(self) -> bool:
        """
        Validate the expiry date's MRZ checksum.

        :return: True if valid, False otherwise
        """
        if self.mrz2.value is None:
            return False
        if PassportV1.check_sum(self.mrz2.value[21:27]) == self.mrz2.value[27]:
            self.expiry_date.confidence = 1.0
            return True
        return False

    def __mrz_personal_number_checksum(self) -> bool:
        """
        Validate the personal number's MRZ checksum.

        :return: True if valid, False otherwise
        """
        if self.mrz2.value is None:
            return False
        return PassportV1.check_sum(self.mrz2.value[28:42]) == self.mrz2.value[42]

    def __mrz_last_name_checksum(self) -> bool:
        """
        Validate the last name's MRZ checksum.

        :return: True if valid, False otherwise
        """
        if self.mrz2.value is None:
            return False
        if (
            PassportV1.check_sum(
                self.mrz2.value[0:10] + self.mrz2.value[13:20] + self.mrz2.value[21:43]
            )
            == self.mrz2.value[43]
        ):
            self.surname.confidence = 1.0
            return True
        return False

    # Reconstruct
    def __reconstruct_mrz(self) -> None:
        """
        Set self.mrz with Field object.

        The mrz Field value is the concatenation of mrz1 and mr2
        The mrz Field confidence is the product of mrz1 and mrz2 probabilities
        """
        if (
            self.mrz1.value is not None
            and self.mrz2.value is not None
            and self.mrz.value is None
        ):
            mrz = {
                "value": self.mrz1.value + self.mrz2.value,
                "confidence": field_array_confidence([self.mrz1, self.mrz2]),
            }
            self.mrz = TextField(mrz, reconstructed=True)

    def __reconstruct_full_name(self) -> None:
        """
        Set self.full_name with Field object.

        The full_name Field value is the concatenation of:
            first given url_name and last url_name
        The full_name Field confidence is the product of:
            first given url_name and last url_name probabilities
        """
        if (
            self.surname.value is not None
            and len(self.given_names) != 0
            and self.given_names[0].value is not None
            and self.full_name.value is None
        ):
            given_names = " ".join(
                [name.value if name.value else "" for name in self.given_names]
            )
            full_name = {
                "value": f"{given_names} {self.surname}",
                "confidence": field_array_confidence(
                    [self.surname, self.given_names[0]]
                ),
            }
            self.full_name = TextField(full_name, reconstructed=True)


TypePassportV1 = TypeVar(
    "TypePassportV1",
    bound=PassportV1,
)
