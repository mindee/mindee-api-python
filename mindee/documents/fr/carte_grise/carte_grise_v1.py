from typing import Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.fields.date import DateField
from mindee.fields.text import TextField


class CarteGriseV1(Document):
    """Carte Grise v1 prediction results."""

    formula_number: TextField
    """Document formula number"""
    mrz1: TextField
    """Machine readable zone first line"""
    mrz2: TextField
    """Machine readable zone second line"""
    owner_first_name: TextField
    """Vehicle's owner first name"""
    owner_surname: TextField
    """Vehicle's owner surname"""
    a: TextField
    """Vehicle license plate number"""
    b: DateField
    """Vehicle first release date"""
    c1: TextField
    """Vehicle's owner full name including maiden name"""
    c3: TextField
    """Vehicle's owner address"""
    c41: TextField
    """Number of owners of the license certificate"""
    c4a: TextField
    """Mention about the ownership of the vehicle"""
    d1: TextField
    """Vehicle brand"""
    d3: TextField
    """vehicle commercial name"""
    e: TextField
    """Vehicle identification number (VIN)"""
    f1: TextField
    """Vehicle's maximum admissible weight"""
    f2: TextField
    """Vehicle's maximum admissible weight within the license's state"""
    f3: TextField
    """Vehicle's maximum authorized weight with coupling"""
    g: TextField
    """Vehicle's weight with coupling if tractor different than category M1"""
    g1: TextField
    """Vehicle's national empty weight"""
    i: DateField
    """Car registration date of the given certificate"""
    j: TextField
    """Vehicle's category"""
    j1: TextField
    """Vehicle's national type"""
    j2: TextField
    """Vehicle's body type (CE)"""
    j3: TextField
    """Vehicle's body type (National designation)"""
    p1: TextField
    """Vehicle's displacement (cm3)"""
    p2: TextField
    """Vehicle's maximum net power (kW)"""
    p3: TextField
    """Vehicle's fuel type"""
    p6: TextField
    """Vehicle's administrative power (fiscal horse power)"""
    q: TextField
    """Vehicle's power / weight ratio"""
    s1: TextField
    """Vehicle's number of seats"""
    s2: TextField
    """Vehicle's number of standing rooms (person)"""
    u1: TextField
    """Vehicle's sound level (dB)"""
    u2: TextField
    """Vehicle's engine rotation speed (min-1)"""
    v7: TextField
    """Vehicle's CO2 emission"""
    x1: DateField
    """Next technical control date"""
    y1: TextField
    """Amount of the regional proportional tax of the gray card (in euros)."""
    y2: TextField
    """Amount of the additional parafiscal tax of the gray card (in euros)."""
    y3: TextField
    """Amount of the additional CO2 tax of the gray card (in euros)."""
    y4: TextField
    """Amount of the fee for managing the registration certificate (in euros)."""
    y5: TextField
    """Amount of the fee for delivery of the registration certificate in euros."""
    y6: TextField
    """Total amount of registration fee to be paid in euros."""

    def __init__(
        self,
        api_prediction=None,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        Bank check document.

        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type="carte_grise",
            api_prediction=api_prediction,
            page_n=page_n,
        )
        self._build_from_api_prediction(api_prediction["prediction"], page_n=page_n)

    def _build_from_api_prediction(
        self, api_prediction: TypeApiPrediction, page_n: Optional[int] = None
    ) -> None:
        """
        Build the document from an API response JSON.

        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number for multi pages pdf input
        """
        # pylint: disable=invalid-name
        self.formula_number = TextField(
            api_prediction["formula_number"], page_id=page_n
        )
        self.mrz1 = TextField(api_prediction["mrz1"], page_id=page_n)
        self.mrz2 = TextField(api_prediction["mrz2"], page_id=page_n)
        self.owner_first_name = TextField(
            api_prediction["owner_first_name"], page_id=page_n
        )
        self.owner_surname = TextField(api_prediction["owner_surname"], page_id=page_n)
        self.a = TextField(api_prediction["a"], page_id=page_n)
        self.b = DateField(api_prediction["b"], page_id=page_n)
        self.c1 = TextField(api_prediction["c1"], page_id=page_n)
        self.c3 = TextField(api_prediction["c3"], page_id=page_n)
        self.c41 = TextField(api_prediction["c41"], page_id=page_n)
        self.c4a = TextField(api_prediction["c4a"], page_id=page_n)
        self.d1 = TextField(api_prediction["d1"], page_id=page_n)
        self.d3 = TextField(api_prediction["d3"], page_id=page_n)
        self.e = TextField(api_prediction["e"], page_id=page_n)
        self.f1 = TextField(api_prediction["f1"], page_id=page_n)
        self.f2 = TextField(api_prediction["f2"], page_id=page_n)
        self.f3 = TextField(api_prediction["f3"], page_id=page_n)
        self.g = TextField(api_prediction["g"], page_id=page_n)
        self.g1 = TextField(api_prediction["g1"], page_id=page_n)
        self.i = DateField(api_prediction["i"], page_id=page_n)
        self.j = TextField(api_prediction["j"], page_id=page_n)
        self.j1 = TextField(api_prediction["j1"], page_id=page_n)
        self.j2 = TextField(api_prediction["j2"], page_id=page_n)
        self.j3 = TextField(api_prediction["j3"], page_id=page_n)
        self.p1 = TextField(api_prediction["p1"], page_id=page_n)
        self.p2 = TextField(api_prediction["p2"], page_id=page_n)
        self.p3 = TextField(api_prediction["p3"], page_id=page_n)
        self.p6 = TextField(api_prediction["p6"], page_id=page_n)
        self.q = TextField(api_prediction["q"], page_id=page_n)
        self.s1 = TextField(api_prediction["s1"], page_id=page_n)
        self.s2 = TextField(api_prediction["s2"], page_id=page_n)
        self.u1 = TextField(api_prediction["u1"], page_id=page_n)
        self.u2 = TextField(api_prediction["u2"], page_id=page_n)
        self.v7 = TextField(api_prediction["v7"], page_id=page_n)
        self.x1 = DateField(api_prediction["x1"], page_id=page_n)
        self.y1 = TextField(api_prediction["y1"], page_id=page_n)
        self.y2 = TextField(api_prediction["y2"], page_id=page_n)
        self.y3 = TextField(api_prediction["y3"], page_id=page_n)
        self.y4 = TextField(api_prediction["y4"], page_id=page_n)
        self.y5 = TextField(api_prediction["y5"], page_id=page_n)
        self.y6 = TextField(api_prediction["y6"], page_id=page_n)

    def __str__(self) -> str:
        return clean_out_string(
            "----- FR Carte Grise V1 -----\n"
            f"Filename: {self.filename or ''}\n"
            f"formula_number: {self.formula_number}\n"
            f"mrz1: {self.mrz1}\n"
            f"mrz2: {self.mrz2}\n"
            f"owner_first_name: {self.owner_first_name}\n"
            f"owner_surname: {self.owner_surname}\n"
            f"a: {self.a}\n"
            f"b: {self.b}\n"
            f"c1: {self.c1}\n"
            f"c3: {self.c3}\n"
            f"c41: {self.c41}\n"
            f"c4a: {self.c4a}\n"
            f"d1: {self.d1}\n"
            f"d3: {self.d3}\n"
            f"e: {self.e}\n"
            f"f1: {self.f1}\n"
            f"f2: {self.f2}\n"
            f"f3: {self.f3}\n"
            f"g: {self.g}\n"
            f"g1: {self.g1}\n"
            f"i: {self.i}\n"
            f"j: {self.j}\n"
            f"j1: {self.j1}\n"
            f"j2: {self.j2}\n"
            f"j3: {self.j3}\n"
            f"p1: {self.p1}\n"
            f"p2: {self.p2}\n"
            f"p3: {self.p3}\n"
            f"p6: {self.p6}\n"
            f"q: {self.q}\n"
            f"s1: {self.s1}\n"
            f"s2: {self.s2}\n"
            f"u1: {self.u1}\n"
            f"u2: {self.u2}\n"
            f"v7: {self.v7}\n"
            f"x1: {self.x1}\n"
            f"y1: {self.y1}\n"
            f"y2: {self.y2}\n"
            f"y3: {self.y3}\n"
            f"y4: {self.y4}\n"
            f"y5: {self.y5}\n"
            f"y6: {self.y6}\n"
            "----------------------"
        )

    def _checklist(self) -> None:
        pass


TypeCarteGriseV1 = TypeVar("TypeCarteGriseV1", bound=CarteGriseV1)
