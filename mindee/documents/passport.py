from typing import List
from datetime import datetime

from mindee.documents.base import Document
from mindee.fields import Field
from mindee.fields.date import Date
from mindee.http import Endpoint


class Passport(Document):
    country: Field
    id_number: Field
    birth_date: Date
    expiry_date: Date
    issuance_date: Date
    birth_place: Field
    gender: Field
    surname: Field
    mrz1: Field
    mrz2: Field
    given_names: List[Field] = []
    mrz: Field
    full_name: Field

    def __init__(
        self,
        api_prediction=None,
        input_file=None,
        page_n=0,
        document_type="passport",
    ):
        """
        :param api_prediction: Raw prediction from HTTP response
        :param input_file: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_file=input_file,
            document_type=document_type,
            api_prediction=api_prediction,
            page_n=page_n,
        )

    def build_from_api_prediction(self, api_prediction, page_n=0):
        """
        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number for multi pages pdf input
        :return: (void) set the object attributes with api prediction values
        """
        self.country = Field(api_prediction["country"], page_n=page_n)
        self.id_number = Field(api_prediction["id_number"], page_n=page_n)
        self.birth_date = Date(api_prediction["birth_date"], "value", page_n=page_n)
        self.expiry_date = Date(api_prediction["expiry_date"], "value", page_n=page_n)
        self.issuance_date = Date(
            api_prediction["issuance_date"], "value", page_n=page_n
        )
        self.birth_place = Field(api_prediction["birth_place"], page_n=page_n)
        self.gender = Field(api_prediction["gender"], page_n=page_n)
        self.surname = Field(api_prediction["surname"], page_n=page_n)
        self.mrz1 = Field(api_prediction["mrz1"], page_n=page_n)
        self.mrz2 = Field(api_prediction["mrz2"], page_n=page_n)
        self.given_names = [
            Field(given_name, page_n=page_n)
            for given_name in api_prediction["given_names"]
        ]
        self.mrz = Field({"value": None, "confidence": 0.0}, page_n=page_n)
        self.full_name = Field({"value": None, "confidence": 0.0}, page_n=page_n)

    def __str__(self) -> str:
        given_names = " ".join(
            [
                given_name.value if given_name.value is not None else ""
                for given_name in self.given_names
            ]
        )
        return (
            "-----Passport data-----\n"
            f"Filename: {self.filename}\n"
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

    def is_expired(self):
        """
        :return: True if the passport is expired, False otherwise
        """
        return self.expiry_date.date_object < datetime.date(datetime.now())

    @staticmethod
    def request(endpoints: List[Endpoint], input_file, include_words=False):
        """
        Make request to expense_receipts endpoint
        :param input_file: Input object
        :param endpoints: Endpoints config
        :param include_words: Include Mindee vision words in http_response
        """
        if include_words:
            raise Exception(
                "invlude_words parameter cannot be set to True for passport API"
            )
        return endpoints[0].predict_request(input_file, include_words)

    def _reconstruct(self):
        """
        Call fields reconstruction methods
        """
        self.__reconstruct_mrz()
        self.__reconstruct_full_name()

    def _checklist(self, *args):
        """
        Call check methods
        """
        self.checklist = {
            "mrz_id_number_checksum": self.__mrz_id_number_checksum(),
            "mrz_date_of_birth_checksum": self.__mrz_date_of_birth_checksum(),
            "mrz_expiration_date_checksum": self.__mrz_expiration_date_checksum(),
            "mrz_personal_number_checksum": self.__mrz_personal_number_checksum(),
            "mrz_last_name_checksum": self.__mrz_last_name_checksum(),
            "mrz_checksum": self.__mrz__checksum(),
        }

    # Checks
    def __mrz__checksum(self):
        """
        :return: True if the all MRZ checksums are validated, False otherwise
        """
        return (
            self.__mrz_id_number_checksum()
            and self.__mrz_date_of_birth_checksum()
            and self.__mrz_expiration_date_checksum()
            and self.__mrz_personal_number_checksum()
            and self.__mrz_last_name_checksum()
        )

    def __mrz_id_number_checksum(self) -> bool:
        """
        :return: True if id number MRZ checksum is validated, False otherwise
        """
        if self.mrz2.value is None:
            return False
        if Passport.check_sum(self.mrz2.value[:9]) == self.mrz2.value[9]:
            self.id_number.confidence = 1.0
            return True
        return False

    def __mrz_date_of_birth_checksum(self) -> bool:
        """
        :return: True if date of birth MRZ checksum is validated, False otherwise
        """
        if self.mrz2.value is None:
            return False
        if Passport.check_sum(self.mrz2.value[13:19]) == self.mrz2.value[19]:
            self.birth_date.confidence = 1.0
            return True
        return False

    def __mrz_expiration_date_checksum(self) -> bool:
        """
        :return: True if expiry date MRZ checksum is validated, False otherwise
        """
        if self.mrz2.value is None:
            return False
        if Passport.check_sum(self.mrz2.value[21:27]) == self.mrz2.value[27]:
            self.expiry_date.confidence = 1.0
            return True
        return False

    def __mrz_personal_number_checksum(self) -> bool:
        """
        :return: True if personal number MRZ checksum is validated, False otherwise
        """
        if self.mrz2.value is None:
            return False
        return Passport.check_sum(self.mrz2.value[28:42]) == self.mrz2.value[42]

    def __mrz_last_name_checksum(self):
        """
        :return: True if last url_name MRZ checksum is validated, False otherwise
        """
        if self.mrz2.value is None:
            return False
        if (
            Passport.check_sum(
                self.mrz2.value[0:10] + self.mrz2.value[13:20] + self.mrz2.value[21:43]
            )
            == self.mrz2.value[43]
        ):
            self.surname.confidence = 1.0
            return True
        return False

    @staticmethod
    def check_sum(to_check: str) -> str:
        """
        https://en.wikipedia.org/wiki/Machine-readable_passport
        :param to_check: string
        :return: checksum value for string s
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

    # Reconstruct
    def __reconstruct_mrz(self):
        """
        Set self.mrz with Field object
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
                "confidence": Field.array_confidence(
                    [self.mrz1.confidence, self.mrz2.confidence]
                ),
            }
            self.mrz = Field(mrz, reconstructed=True)

    def __reconstruct_full_name(self):
        """
        Set self.full_name with Field object
        The full_name Field value is the concatenation of first given url_name and last url_name
        The full_name Field confidence is the product of first given url_name and last url_name probabilities
        """
        if (
            self.surname.value is not None
            and len(self.given_names) != 0
            and self.given_names[0].value is not None
            and self.full_name.value is None
        ):
            full_name = {
                "value": self.given_names[0].value + " " + self.surname.value,
                "confidence": Field.array_confidence(
                    [self.surname.confidence, self.given_names[0].confidence]
                ),
            }
            self.full_name = Field(full_name, reconstructed=True)
