from datetime import datetime

from mindee.documents.base import Document, OFF_THE_SHELF
from mindee.fields import Field
from mindee.fields.date import Date
from mindee.http import make_api_request, make_predict_url
from mindee.documents.document_config import DocumentConfig


class Passport(Document):
    def __init__(
        self,
        api_prediction=None,
        input_file=None,
        country=None,
        id_number=None,
        birth_date=None,
        expiry_date=None,
        issuance_date=None,
        birth_place=None,
        gender=None,
        surname=None,
        mrz1=None,
        mrz2=None,
        given_names=None,
        mrz=None,
        full_name=None,
        page_n=0,
        document_type="passport",
    ):
        """
        :param api_prediction: Raw prediction from HTTP response
        :param input_file: Input object
        :param country: country value for creating Passport object from scratch
        :param id_number: id_number value for creating Passport object from scratch
        :param birth_date: birth_date value for creating Passport object from scratch
        :param expiry_date: expiry_date value for creating Passport object from scratch
        :param issuance_date: issuance_date value for creating Passport object from scratch
        :param birth_place: birth_place value for creating Passport object from scratch
        :param gender: gender value for creating Passport object from scratch
        :param surname: surname value for creating Passport object from scratch
        :param mrz1: mrz1 value for creating Passport object from scratch
        :param mrz2: mrz2 value for creating Passport object from scratch
        :param given_names: given_names value for creating Passport object from scratch
        :param mrz: mrz value for creating Passport object from scratch
        :param full_name: full_name value for creating Passport object from scratch
        :param page_n: Page number for multi pages pdf input
        """
        # Raw data
        self.type = document_type
        self.country = None
        self.id_number = None
        self.birth_date = None
        self.expiry_date = None
        self.issuance_date = None
        self.birth_place = None
        self.gender = None
        self.surname = None
        self.mrz1 = None
        self.mrz2 = None
        self.given_names = []
        self.mrz = None
        self.full_name = None

        if api_prediction is not None:
            self.build_from_api_prediction(api_prediction)
        else:
            self.country = Field({"value": country}, value_key="value", page_n=page_n)
            self.id_number = Field(
                {"value": id_number}, value_key="value", page_n=page_n
            )
            self.birth_date = Date(
                {"value": birth_date}, value_key="value", page_n=page_n
            )
            self.expiry_date = Date(
                {"value": expiry_date}, value_key="value", page_n=page_n
            )
            self.issuance_date = Date(
                {"value": issuance_date}, value_key="value", page_n=page_n
            )
            self.birth_place = Field(
                {"value": birth_place}, value_key="value", page_n=page_n
            )
            self.gender = Field({"value": gender}, value_key="value", page_n=page_n)
            self.surname = Field({"value": surname}, value_key="value", page_n=page_n)
            self.mrz1 = Field({"value": mrz1}, value_key="value", page_n=page_n)
            self.mrz2 = Field({"value": mrz2}, value_key="value", page_n=page_n)
            if given_names is not None:
                self.given_names = [
                    Field({"value": g}, value_key="value", page_n=page_n)
                    for g in given_names
                ]
            self.mrz = Field({"value": mrz}, value_key="value", page_n=page_n)
            self.full_name = Field(
                {"value": full_name}, value_key="value", page_n=page_n
            )

        # Invoke Document constructor
        super().__init__(input_file)

        # Run checks
        self._checklist()

        # Reconstruct extra fields
        self._reconstruct()

    @staticmethod
    def get_document_config() -> DocumentConfig:
        """:return: the configuration for passport"""
        return DocumentConfig(
            {
                "constructor": Passport,
                "api_key_kwargs": ["passport_api_key"],
                "document_type": "passport",
                "singular_name": "passport",
                "plural_name": "passports",
            },
            doc_type=OFF_THE_SHELF,
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
        return (
            "-----Passport data-----\n"
            "Filename: %s \n"
            "Full name: %s \n"
            "Given names: %s \n"
            "Surname: %s\n"
            "Country: %s\n"
            "ID Number: %s\n"
            "Issuance date: %s\n"
            "Birth date: %s\n"
            "Expiry date: %s\n"
            "MRZ 1: %s\n"
            "MRZ 2: %s\n"
            "MRZ: %s\n"
            "----------------------"
            % (
                self.filename,
                self.full_name.value,
                " ".join(
                    [
                        given_name.value if given_name.value is not None else ""
                        for given_name in self.given_names
                    ]
                ),
                self.surname.value,
                self.country.value,
                self.id_number.value,
                self.issuance_date.value,
                self.birth_date.value,
                self.expiry_date.value,
                self.mrz1.value,
                self.mrz2.value,
                self.mrz.value,
            )
        )

    def is_expired(self):
        """
        :return: True if the passport is expired, False otherwise
        """
        return self.expiry_date.date_object < datetime.date(datetime.now())

    @staticmethod
    def request(client, input_file, version="1", include_words=False):
        """
        Make request to passport endpoint
        """
        if include_words:
            raise Exception(
                "invlude_words parameter cannot be set to True for passport API"
            )

        url = make_predict_url("passport", version)
        return make_api_request(url, input_file, client.passport_api_key)

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
            self.id_number.probability = 1.0
            return True
        return False

    def __mrz_date_of_birth_checksum(self) -> bool:
        """
        :return: True if date of birth MRZ checksum is validated, False otherwise
        """
        if self.mrz2.value is None:
            return False
        if Passport.check_sum(self.mrz2.value[13:19]) == self.mrz2.value[19]:
            self.birth_date.probability = 1.0
            return True
        return False

    def __mrz_expiration_date_checksum(self) -> bool:
        """
        :return: True if expiry date MRZ checksum is validated, False otherwise
        """
        if self.mrz2.value is None:
            return False
        if Passport.check_sum(self.mrz2.value[21:27]) == self.mrz2.value[27]:
            self.expiry_date.probability = 1.0
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
        :return: True if last name MRZ checksum is validated, False otherwise
        """
        if self.mrz2.value is None:
            return False
        if (
            Passport.check_sum(
                self.mrz2.value[0:10] + self.mrz2.value[13:20] + self.mrz2.value[21:43]
            )
            == self.mrz2.value[43]
        ):
            self.surname.probability = 1.0
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
        The mrz Field probability is the product of mrz1 and mrz2 probabilities
        """
        if (
            self.mrz1.value is not None
            and self.mrz2.value is not None
            and self.mrz.value is None
        ):
            mrz = {
                "value": self.mrz1.value + self.mrz2.value,
                "confidence": Field.array_probability(
                    [self.mrz1.probability, self.mrz2.probability]
                ),
            }
            self.mrz = Field(mrz, reconstructed=True)

    def __reconstruct_full_name(self):
        """
        Set self.full_name with Field object
        The full_name Field value is the concatenation of first given name and last name
        The full_name Field probability is the product of first given name and last name probabilities
        """
        if (
            self.surname.value is not None
            and len(self.given_names) != 0
            and self.given_names[0].value is not None
            and self.full_name.value is None
        ):
            full_name = {
                "value": self.given_names[0].value + " " + self.surname.value,
                "confidence": Field.array_probability(
                    [self.surname.probability, self.given_names[0].probability]
                ),
            }
            self.full_name = Field(full_name, reconstructed=True)
