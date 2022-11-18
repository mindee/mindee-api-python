from datetime import datetime
from typing import List, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.base import field_array_confidence
from mindee.fields.date import DateField
from mindee.fields.text import TextField


class PassportV1(Document):
    country: TextField
    """Country of issue"""
    id_number: TextField
    """Passport number"""
    expiry_date: DateField
    """Date the passport expires"""
    issuance_date: DateField
    """Date the passport was issued"""
    surname: TextField
    """Holder's last name (surname)"""
    given_names: List[TextField]
    """Holder's list of first (given) names"""
    full_name: TextField
    """
    Holder's full name.
    The combination of `given_names` and `surname` fields.
    """
    birth_date: DateField
    """Holder's date of birth"""
    birth_place: TextField
    """Holder's place of birth"""
    gender: TextField
    """Holder's gender or sex"""
    mrz1: TextField
    """First line of the Machine-Readable Zone"""
    mrz2: TextField
    """Second line of the Machine-Readable Zone"""
    mrz: TextField
    """Combination of both MRZ fields."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
        document_type="passport",
    ):
        """
        Passport document.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type=document_type,
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
        Build the document from an API response JSON.

        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number for multi pages pdf input
        """
        self.country = TextField(api_prediction["country"], page_n=page_n)
        self.id_number = TextField(api_prediction["id_number"], page_n=page_n)
        self.birth_date = DateField(api_prediction["birth_date"], page_n=page_n)
        self.expiry_date = DateField(api_prediction["expiry_date"], page_n=page_n)
        self.issuance_date = DateField(api_prediction["issuance_date"], page_n=page_n)
        self.birth_place = TextField(api_prediction["birth_place"], page_n=page_n)
        self.gender = TextField(api_prediction["gender"], page_n=page_n)
        self.surname = TextField(api_prediction["surname"], page_n=page_n)
        self.mrz1 = TextField(api_prediction["mrz1"], page_n=page_n)
        self.mrz2 = TextField(api_prediction["mrz2"], page_n=page_n)
        self.given_names = [
            TextField(given_name, page_n=page_n)
            for given_name in api_prediction["given_names"]
        ]
        self.mrz = TextField({"value": None, "confidence": 0.0}, page_n=page_n)
        self.full_name = TextField({"value": None, "confidence": 0.0}, page_n=page_n)

    def __str__(self) -> str:
        given_names = " ".join(
            [
                given_name.value if given_name.value is not None else ""
                for given_name in self.given_names
            ]
        )
        return clean_out_string(
            "-----Passport data-----\n"
            f"Filename: {self.filename or ''}\n"
            f"Full name: {self.full_name}\n"
            f"Given names: {given_names}\n"
            f"Surname: {self.surname}\n"
            f"Country: {self.country}\n"
            f"ID Number: {self.id_number}\n"
            f"Issuance date: {self.issuance_date}\n"
            f"Birth date: {self.birth_date}\n"
            f"Expiry date: {self.expiry_date}\n"
            f"MRZ 1: {self.mrz1}\n"
            f"MRZ 2: {self.mrz2}\n"
            f"MRZ: {self.mrz}\n"
            "----------------------"
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
            full_name = {
                "value": self.given_names[0].value + " " + self.surname.value,
                "confidence": field_array_confidence(
                    [self.surname, self.given_names[0]]
                ),
            }
            self.full_name = TextField(full_name, reconstructed=True)


TypePassportV1 = TypeVar("TypePassportV1", bound=PassportV1)
