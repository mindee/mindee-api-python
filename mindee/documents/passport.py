from mindee.benchmark import Benchmark
from mindee.documents import Document
from mindee.fields import Field
from mindee.fields.date import Date
from datetime import datetime
from mindee.http import request
import os


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
            page_n=0
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
        self.type = "Passport"
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
            self.id_number = Field({"value": id_number}, value_key="value", page_n=page_n)
            self.birth_date = Date({"value": birth_date}, value_key="value", page_n=page_n)
            self.expiry_date = Date({"value": expiry_date}, value_key="value", page_n=page_n)
            self.issuance_date = Date({"value": issuance_date}, value_key="value", page_n=page_n)
            self.birth_place = Field({"value": birth_place}, value_key="value", page_n=page_n)
            self.gender = Field({"value": gender}, value_key="value", page_n=page_n)
            self.surname = Field({"value": surname}, value_key="value", page_n=page_n)
            self.mrz1 = Field({"value": mrz1}, value_key="value", page_n=page_n)
            self.mrz2 = Field({"value": mrz2}, value_key="value", page_n=page_n)
            if given_names is not None:
                self.given_names = [Field({"value": g}, value_key="value", page_n=page_n) for g in given_names]
            self.mrz = Field({"value": mrz}, value_key="value", page_n=page_n)
            self.full_name = Field({"value": full_name}, value_key="value", page_n=page_n)

        # Invoke Document constructor
        super(Passport, self).__init__(input_file)

        # Run checks
        self._checklist()

        # Reconstruct extra fields
        self._reconstruct()

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
        self.issuance_date = Date(api_prediction["issuance_date"], "value", page_n=page_n)
        self.birth_place = Field(api_prediction["birth_place"], page_n=page_n)
        self.gender = Field(api_prediction["gender"], page_n=page_n)
        self.surname = Field(api_prediction["surname"], page_n=page_n)
        self.mrz1 = Field(api_prediction["mrz1"], page_n=page_n)
        self.mrz2 = Field(api_prediction["mrz2"], page_n=page_n)
        self.given_names = [Field(given_name, page_n=page_n) for given_name in api_prediction["given_names"]]
        self.mrz = Field({"value": None, "probability": 0.}, page_n=page_n)
        self.full_name = Field({"value": None, "probability": 0.}, page_n=page_n)

    def __str__(self):
        return "-----Passport data-----\n" \
               "Filename: %s \n" \
               "Full name: %s \n" \
               "Given names: %s \n" \
               "Surname: %s\n" \
               "Country: %s\n" \
               "ID Number: %s\n" \
               "Issuance date: %s\n" \
               "Birth date: %s\n" \
               "Expiry date: %s\n" \
               "MRZ 1: %s\n" \
               "MRZ 2: %s\n" \
               "MRZ: %s\n" \
               "----------------------" % \
               (
                   self.filename,
                   self.full_name.value,
                   " ".join(
                       [given_name.value if given_name.value is not None else "" for given_name in self.given_names]),
                   self.surname.value,
                   self.country.value,
                   self.id_number.value,
                   self.issuance_date.value,
                   self.birth_date.value,
                   self.expiry_date.value,
                   self.mrz1.value,
                   self.mrz2.value,
                   self.mrz.value
               )

    @staticmethod
    def compare(passport=None, ground_truth=None):
        """
        :param passport: Passport object to compare
        :param ground_truth: Ground truth Passport object
        :return: Accuracy and precisions metrics
        """
        assert passport is not None
        assert ground_truth is not None
        assert isinstance(passport, Passport)
        assert isinstance(ground_truth, Passport)

        metrics = {}

        # Compute Accuracy metrics
        metrics.update(Passport.compute_accuracy(passport, ground_truth))

        # Compute precision metrics
        metrics.update(Passport.compute_precision(passport, ground_truth))

        return metrics

    def is_expired(self):
        """
        :return: True if the passport is expired, False otherwise
        """
        return self.expiry_date.date_object < datetime.date(datetime.now())

    @staticmethod
    def request(input_file, base_url, passport_token=None, version="1"):
        """
        Make request to passport endpoint
        """
        url = os.path.join(base_url, "passport", "v" + version, "predict")
        return request(url, input_file, passport_token)

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
            "mrz_checksum": self.__mrz__checksum()
        }

    # Checks
    def __mrz__checksum(self):
        """
        :return: True if the all MRZ checksums are validated, False otherwise
        """
        return self.__mrz_id_number_checksum() and \
               self.__mrz_date_of_birth_checksum() and \
               self.__mrz_expiration_date_checksum() and \
               self.__mrz_personal_number_checksum() and \
               self.__mrz_last_name_checksum()

    def __mrz_id_number_checksum(self):
        """
        :return: True if id number MRZ checksum is validated, False otherwise
        """
        if self.mrz2.value is None:
            return False
        if Passport.check_sum(self.mrz2.value[:9]) == self.mrz2.value[9]:
            self.id_number.probability = 1.
            return True

    def __mrz_date_of_birth_checksum(self):
        """
        :return: True if date of birth MRZ checksum is validated, False otherwise
        """
        if self.mrz2.value is None:
            return False
        if Passport.check_sum(self.mrz2.value[13:19]) == self.mrz2.value[19]:
            self.birth_date.probability = 1.
            return True

    def __mrz_expiration_date_checksum(self):
        """
        :return: True if expiry date MRZ checksum is validated, False otherwise
        """
        if self.mrz2.value is None:
            return False
        if Passport.check_sum(self.mrz2.value[21:27]) == self.mrz2.value[27]:
            self.expiry_date.probability = 1.
            return True

    def __mrz_personal_number_checksum(self):
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
        if Passport.check_sum(self.mrz2.value[0:10] + self.mrz2.value[13:20] + self.mrz2.value[21:43]) == \
                self.mrz2.value[43]:
            self.surname.probability = 1.
            return True

    @staticmethod
    def check_sum(s):
        """
        https://en.wikipedia.org/wiki/Machine-readable_passport
        :param s: string
        :return: checksum value for string s
        """
        checker = 0
        alpha_to_num = {c: 10 + i for i, c in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}
        for i, c in enumerate(s):
            if i % 3 == 0:
                weight = 7
            elif i % 3 == 1:
                weight = 3
            else:
                weight = 1

            if c == '<':
                val = 0
            elif c.isalpha():
                val = alpha_to_num[c]
            else:
                val = int(c)
            checker += val * weight
        return str(checker % 10)

    # Reconstruct
    def __reconstruct_mrz(self):
        """
        Set self.mrz with Field object
        The mrz Field value is the concatenation of mrz1 and mr2
        The mrz Field probability is the product of mrz1 and mrz2 probabilities
        """
        if self.mrz1.value is not None \
                and self.mrz2.value is not None \
                and self.mrz.value is None:
            mrz = {
                "value": self.mrz1.value + self.mrz2.value,
                "probability": Field.array_probability([self.mrz1.probability, self.mrz2.probability])
            }
            self.mrz = Field(mrz, reconstructed=True)

    def __reconstruct_full_name(self):
        """
        Set self.full_name with Field object
        The full_name Field value is the concatenation of first given name and last name
        The full_name Field probability is the product of first given name and last name probabilities
        """
        if self.surname.value is not None \
                and len(self.given_names) != 0 \
                and self.given_names[0].value is not None \
                and self.full_name.value is None:
            full_name = {
                "value": self.given_names[0].value + " " + self.surname.value,
                "probability": Field.array_probability([self.surname.probability, self.given_names[0].probability])
            }
            self.full_name = Field(full_name, reconstructed=True)

    @staticmethod
    def compute_accuracy(passport, ground_truth):
        """
        :param passport: Passport object to compare
        :param ground_truth: Ground truth Passport object
        :return: Accuracy metrics
        """
        return {
            "__acc__country": ground_truth.country == passport.country,
            "__acc__id_number": ground_truth.id_number == passport.id_number,
            "__acc__birth_date": ground_truth.birth_date == passport.birth_date,
            "__acc__expiry_date": ground_truth.expiry_date == passport.expiry_date,
            "__acc__issuance_date": ground_truth.issuance_date == passport.issuance_date,
            "__acc__gender": ground_truth.gender == passport.gender,
            "__acc__surname": ground_truth.surname == passport.surname,
            "__acc__mrz1": ground_truth.mrz1 == passport.mrz1,
            "__acc__mrz2": ground_truth.mrz2 == passport.mrz2,
            "__acc__given_names": Field.compare_arrays(passport.given_names, ground_truth.given_names),
            "__acc__mrz": ground_truth.mrz == passport.mrz,
            "__acc__full_name": ground_truth.full_name == passport.full_name,
        }

    @staticmethod
    def compute_precision(passport, ground_truth):
        """
        :param passport: Passport object to compare
        :param ground_truth: Ground truth Passport object
        :return: Precision metrics
        """
        precisions = {
            "__pre__country": Benchmark.scalar_precision_score(passport.country, ground_truth.country),
            "__pre__id_number": Benchmark.scalar_precision_score(passport.id_number, ground_truth.id_number),
            "__pre__birth_date": Benchmark.scalar_precision_score(passport.birth_date, ground_truth.birth_date),
            "__pre__expiry_date": Benchmark.scalar_precision_score(passport.expiry_date, ground_truth.expiry_date),
            "__pre__issuance_date": Benchmark.scalar_precision_score(passport.issuance_date,
                                                                     ground_truth.issuance_date),
            "__pre__gender": Benchmark.scalar_precision_score(passport.gender, ground_truth.gender),
            "__pre__surname": Benchmark.scalar_precision_score(passport.surname, ground_truth.surname),
            "__pre__mrz1": Benchmark.scalar_precision_score(passport.mrz1, ground_truth.mrz1),
            "__pre__mrz2": Benchmark.scalar_precision_score(passport.mrz2, ground_truth.mrz2),
            "__pre__mrz": Benchmark.scalar_precision_score(passport.mrz, ground_truth.mrz),
            "__pre__full_name": Benchmark.scalar_precision_score(passport.full_name, ground_truth.full_name),
        }

        if len(passport.given_names) == 0:
            precisions["__pre__given_names"] = None
        else:
            precisions["__pre__given_names"] = Field.compare_arrays(passport.given_names, ground_truth.given_names)

        return precisions
