from typing import List, Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.classification import ClassificationField
from mindee.parsing.standard.text import StringField
from mindee.product.resume.resume_v1_certificate import ResumeV1Certificate
from mindee.product.resume.resume_v1_education import ResumeV1Education
from mindee.product.resume.resume_v1_language import ResumeV1Language
from mindee.product.resume.resume_v1_professional_experience import (
    ResumeV1ProfessionalExperience,
)
from mindee.product.resume.resume_v1_social_networks_url import (
    ResumeV1SocialNetworksUrl,
)


class ResumeV1Document(Prediction):
    """Resume API version 1.2 document data."""

    address: StringField
    """The location information of the candidate, including city, state, and country."""
    certificates: List[ResumeV1Certificate]
    """The list of certificates obtained by the candidate."""
    document_language: StringField
    """The ISO 639 code of the language in which the document is written."""
    document_type: ClassificationField
    """The type of the document sent."""
    education: List[ResumeV1Education]
    """The list of the candidate's educational background."""
    email_address: StringField
    """The email address of the candidate."""
    given_names: List[StringField]
    """The candidate's first or given names."""
    hard_skills: List[StringField]
    """The list of the candidate's technical abilities and knowledge."""
    job_applied: StringField
    """The position that the candidate is applying for."""
    languages: List[ResumeV1Language]
    """The list of languages that the candidate is proficient in."""
    nationality: StringField
    """The ISO 3166 code for the country of citizenship of the candidate."""
    phone_number: StringField
    """The phone number of the candidate."""
    profession: StringField
    """The candidate's current profession."""
    professional_experiences: List[ResumeV1ProfessionalExperience]
    """The list of the candidate's professional experiences."""
    social_networks_urls: List[ResumeV1SocialNetworksUrl]
    """The list of social network profiles of the candidate."""
    soft_skills: List[StringField]
    """The list of the candidate's interpersonal and communication abilities."""
    surnames: List[StringField]
    """The candidate's last names."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Resume document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
        self.address = StringField(
            raw_prediction["address"],
            page_id=page_id,
        )
        self.certificates = [
            ResumeV1Certificate(prediction, page_id=page_id)
            for prediction in raw_prediction["certificates"]
        ]
        self.document_language = StringField(
            raw_prediction["document_language"],
            page_id=page_id,
        )
        self.document_type = ClassificationField(
            raw_prediction["document_type"],
            page_id=page_id,
        )
        self.education = [
            ResumeV1Education(prediction, page_id=page_id)
            for prediction in raw_prediction["education"]
        ]
        self.email_address = StringField(
            raw_prediction["email_address"],
            page_id=page_id,
        )
        self.given_names = [
            StringField(prediction, page_id=page_id)
            for prediction in raw_prediction["given_names"]
        ]
        self.hard_skills = [
            StringField(prediction, page_id=page_id)
            for prediction in raw_prediction["hard_skills"]
        ]
        self.job_applied = StringField(
            raw_prediction["job_applied"],
            page_id=page_id,
        )
        self.languages = [
            ResumeV1Language(prediction, page_id=page_id)
            for prediction in raw_prediction["languages"]
        ]
        self.nationality = StringField(
            raw_prediction["nationality"],
            page_id=page_id,
        )
        self.phone_number = StringField(
            raw_prediction["phone_number"],
            page_id=page_id,
        )
        self.profession = StringField(
            raw_prediction["profession"],
            page_id=page_id,
        )
        self.professional_experiences = [
            ResumeV1ProfessionalExperience(prediction, page_id=page_id)
            for prediction in raw_prediction["professional_experiences"]
        ]
        self.social_networks_urls = [
            ResumeV1SocialNetworksUrl(prediction, page_id=page_id)
            for prediction in raw_prediction["social_networks_urls"]
        ]
        self.soft_skills = [
            StringField(prediction, page_id=page_id)
            for prediction in raw_prediction["soft_skills"]
        ]
        self.surnames = [
            StringField(prediction, page_id=page_id)
            for prediction in raw_prediction["surnames"]
        ]

    @staticmethod
    def _social_networks_urls_separator(char: str) -> str:
        out_str = "  "
        out_str += f"+{char * 22}"
        out_str += f"+{char * 52}"
        return out_str + "+"

    def _social_networks_urls_to_str(self) -> str:
        if not self.social_networks_urls:
            return ""

        lines = f"\n{self._social_networks_urls_separator('-')}\n  ".join(
            [item.to_table_line() for item in self.social_networks_urls]
        )
        out_str = ""
        out_str += f"\n{self._social_networks_urls_separator('-')}\n "
        out_str += " | Name                "
        out_str += " | URL                                               "
        out_str += f" |\n{self._social_networks_urls_separator('=')}"
        out_str += f"\n  {lines}"
        out_str += f"\n{self._social_networks_urls_separator('-')}"
        return out_str

    @staticmethod
    def _languages_separator(char: str) -> str:
        out_str = "  "
        out_str += f"+{char * 10}"
        out_str += f"+{char * 22}"
        return out_str + "+"

    def _languages_to_str(self) -> str:
        if not self.languages:
            return ""

        lines = f"\n{self._languages_separator('-')}\n  ".join(
            [item.to_table_line() for item in self.languages]
        )
        out_str = ""
        out_str += f"\n{self._languages_separator('-')}\n "
        out_str += " | Language"
        out_str += " | Level               "
        out_str += f" |\n{self._languages_separator('=')}"
        out_str += f"\n  {lines}"
        out_str += f"\n{self._languages_separator('-')}"
        return out_str

    @staticmethod
    def _education_separator(char: str) -> str:
        out_str = "  "
        out_str += f"+{char * 17}"
        out_str += f"+{char * 27}"
        out_str += f"+{char * 11}"
        out_str += f"+{char * 10}"
        out_str += f"+{char * 27}"
        out_str += f"+{char * 13}"
        out_str += f"+{char * 12}"
        return out_str + "+"

    def _education_to_str(self) -> str:
        if not self.education:
            return ""

        lines = f"\n{self._education_separator('-')}\n  ".join(
            [item.to_table_line() for item in self.education]
        )
        out_str = ""
        out_str += f"\n{self._education_separator('-')}\n "
        out_str += " | Domain         "
        out_str += " | Degree                   "
        out_str += " | End Month"
        out_str += " | End Year"
        out_str += " | School                   "
        out_str += " | Start Month"
        out_str += " | Start Year"
        out_str += f" |\n{self._education_separator('=')}"
        out_str += f"\n  {lines}"
        out_str += f"\n{self._education_separator('-')}"
        return out_str

    @staticmethod
    def _professional_experiences_separator(char: str) -> str:
        out_str = "  "
        out_str += f"+{char * 17}"
        out_str += f"+{char * 12}"
        out_str += f"+{char * 38}"
        out_str += f"+{char * 27}"
        out_str += f"+{char * 11}"
        out_str += f"+{char * 10}"
        out_str += f"+{char * 22}"
        out_str += f"+{char * 13}"
        out_str += f"+{char * 12}"
        return out_str + "+"

    def _professional_experiences_to_str(self) -> str:
        if not self.professional_experiences:
            return ""

        lines = f"\n{self._professional_experiences_separator('-')}\n  ".join(
            [item.to_table_line() for item in self.professional_experiences]
        )
        out_str = ""
        out_str += f"\n{self._professional_experiences_separator('-')}\n "
        out_str += " | Contract Type  "
        out_str += " | Department"
        out_str += " | Description                         "
        out_str += " | Employer                 "
        out_str += " | End Month"
        out_str += " | End Year"
        out_str += " | Role                "
        out_str += " | Start Month"
        out_str += " | Start Year"
        out_str += f" |\n{self._professional_experiences_separator('=')}"
        out_str += f"\n  {lines}"
        out_str += f"\n{self._professional_experiences_separator('-')}"
        return out_str

    @staticmethod
    def _certificates_separator(char: str) -> str:
        out_str = "  "
        out_str += f"+{char * 12}"
        out_str += f"+{char * 32}"
        out_str += f"+{char * 27}"
        out_str += f"+{char * 6}"
        return out_str + "+"

    def _certificates_to_str(self) -> str:
        if not self.certificates:
            return ""

        lines = f"\n{self._certificates_separator('-')}\n  ".join(
            [item.to_table_line() for item in self.certificates]
        )
        out_str = ""
        out_str += f"\n{self._certificates_separator('-')}\n "
        out_str += " | Grade     "
        out_str += " | Name                          "
        out_str += " | Provider                 "
        out_str += " | Year"
        out_str += f" |\n{self._certificates_separator('=')}"
        out_str += f"\n  {lines}"
        out_str += f"\n{self._certificates_separator('-')}"
        return out_str

    def __str__(self) -> str:
        given_names = f"\n { ' ' * 13 }".join(
            [str(item) for item in self.given_names],
        )
        hard_skills = f"\n { ' ' * 13 }".join(
            [str(item) for item in self.hard_skills],
        )
        soft_skills = f"\n { ' ' * 13 }".join(
            [str(item) for item in self.soft_skills],
        )
        surnames = f"\n { ' ' * 10 }".join(
            [str(item) for item in self.surnames],
        )
        out_str: str = f":Document Language: {self.document_language}\n"
        out_str += f":Document Type: {self.document_type}\n"
        out_str += f":Given Names: {given_names}\n"
        out_str += f":Surnames: {surnames}\n"
        out_str += f":Nationality: {self.nationality}\n"
        out_str += f":Email Address: {self.email_address}\n"
        out_str += f":Phone Number: {self.phone_number}\n"
        out_str += f":Address: {self.address}\n"
        out_str += f":Social Networks: {self._social_networks_urls_to_str()}\n"
        out_str += f":Profession: {self.profession}\n"
        out_str += f":Job Applied: {self.job_applied}\n"
        out_str += f":Languages: {self._languages_to_str()}\n"
        out_str += f":Hard Skills: {hard_skills}\n"
        out_str += f":Soft Skills: {soft_skills}\n"
        out_str += f":Education: {self._education_to_str()}\n"
        out_str += (
            f":Professional Experiences: {self._professional_experiences_to_str()}\n"
        )
        out_str += f":Certificates: {self._certificates_to_str()}\n"
        return clean_out_string(out_str)
