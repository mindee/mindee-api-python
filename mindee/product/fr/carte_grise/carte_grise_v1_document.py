from typing import Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.date import DateField
from mindee.parsing.standard.text import StringField


class CarteGriseV1Document(Prediction):
    """Carte Grise API version 1.1 document data."""

    a: StringField
    """The vehicle's license plate number."""
    b: DateField
    """The vehicle's first release date."""
    c1: StringField
    """The vehicle owner's full name including maiden name."""
    c3: StringField
    """The vehicle owner's address."""
    c41: StringField
    """Number of owners of the license certificate."""
    c4a: StringField
    """Mentions about the ownership of the vehicle."""
    d1: StringField
    """The vehicle's brand."""
    d3: StringField
    """The vehicle's commercial name."""
    e: StringField
    """The Vehicle Identification Number (VIN)."""
    f1: StringField
    """The vehicle's maximum admissible weight."""
    f2: StringField
    """The vehicle's maximum admissible weight within the license's state."""
    f3: StringField
    """The vehicle's maximum authorized weight with coupling."""
    formula_number: StringField
    """The document's formula number."""
    g: StringField
    """The vehicle's weight with coupling if tractor different than category M1."""
    g1: StringField
    """The vehicle's national empty weight."""
    i: DateField
    """The car registration date of the given certificate."""
    j: StringField
    """The vehicle's category."""
    j1: StringField
    """The vehicle's national type."""
    j2: StringField
    """The vehicle's body type (CE)."""
    j3: StringField
    """The vehicle's body type (National designation)."""
    mrz1: StringField
    """Machine Readable Zone, first line."""
    mrz2: StringField
    """Machine Readable Zone, second line."""
    owner_first_name: StringField
    """The vehicle's owner first name."""
    owner_surname: StringField
    """The vehicle's owner surname."""
    p1: StringField
    """The vehicle engine's displacement (cm3)."""
    p2: StringField
    """The vehicle's maximum net power (kW)."""
    p3: StringField
    """The vehicle's fuel type or energy source."""
    p6: StringField
    """The vehicle's administrative power (fiscal horsepower)."""
    q: StringField
    """The vehicle's power to weight ratio."""
    s1: StringField
    """The vehicle's number of seats."""
    s2: StringField
    """The vehicle's number of standing rooms (person)."""
    u1: StringField
    """The vehicle's sound level (dB)."""
    u2: StringField
    """The vehicle engine's rotation speed (RPM)."""
    v7: StringField
    """The vehicle's CO2 emission (g/km)."""
    x1: StringField
    """Next technical control date."""
    y1: StringField
    """Amount of the regional proportional tax of the registration (in euros)."""
    y2: StringField
    """Amount of the additional parafiscal tax of the registration (in euros)."""
    y3: StringField
    """Amount of the additional CO2 tax of the registration (in euros)."""
    y4: StringField
    """Amount of the fee for managing the registration (in euros)."""
    y5: StringField
    """Amount of the fee for delivery of the registration certificate in euros."""
    y6: StringField
    """Total amount of registration fee to be paid in euros."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Carte Grise document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
        self.a = StringField(
            raw_prediction["a"],
            page_id=page_id,
        )
        self.b = DateField(
            raw_prediction["b"],
            page_id=page_id,
        )
        self.c1 = StringField(
            raw_prediction["c1"],
            page_id=page_id,
        )
        self.c3 = StringField(
            raw_prediction["c3"],
            page_id=page_id,
        )
        self.c41 = StringField(
            raw_prediction["c41"],
            page_id=page_id,
        )
        self.c4a = StringField(
            raw_prediction["c4a"],
            page_id=page_id,
        )
        self.d1 = StringField(
            raw_prediction["d1"],
            page_id=page_id,
        )
        self.d3 = StringField(
            raw_prediction["d3"],
            page_id=page_id,
        )
        self.e = StringField(
            raw_prediction["e"],
            page_id=page_id,
        )
        self.f1 = StringField(
            raw_prediction["f1"],
            page_id=page_id,
        )
        self.f2 = StringField(
            raw_prediction["f2"],
            page_id=page_id,
        )
        self.f3 = StringField(
            raw_prediction["f3"],
            page_id=page_id,
        )
        self.formula_number = StringField(
            raw_prediction["formula_number"],
            page_id=page_id,
        )
        self.g = StringField(
            raw_prediction["g"],
            page_id=page_id,
        )
        self.g1 = StringField(
            raw_prediction["g1"],
            page_id=page_id,
        )
        self.i = DateField(
            raw_prediction["i"],
            page_id=page_id,
        )
        self.j = StringField(
            raw_prediction["j"],
            page_id=page_id,
        )
        self.j1 = StringField(
            raw_prediction["j1"],
            page_id=page_id,
        )
        self.j2 = StringField(
            raw_prediction["j2"],
            page_id=page_id,
        )
        self.j3 = StringField(
            raw_prediction["j3"],
            page_id=page_id,
        )
        self.mrz1 = StringField(
            raw_prediction["mrz1"],
            page_id=page_id,
        )
        self.mrz2 = StringField(
            raw_prediction["mrz2"],
            page_id=page_id,
        )
        self.owner_first_name = StringField(
            raw_prediction["owner_first_name"],
            page_id=page_id,
        )
        self.owner_surname = StringField(
            raw_prediction["owner_surname"],
            page_id=page_id,
        )
        self.p1 = StringField(
            raw_prediction["p1"],
            page_id=page_id,
        )
        self.p2 = StringField(
            raw_prediction["p2"],
            page_id=page_id,
        )
        self.p3 = StringField(
            raw_prediction["p3"],
            page_id=page_id,
        )
        self.p6 = StringField(
            raw_prediction["p6"],
            page_id=page_id,
        )
        self.q = StringField(
            raw_prediction["q"],
            page_id=page_id,
        )
        self.s1 = StringField(
            raw_prediction["s1"],
            page_id=page_id,
        )
        self.s2 = StringField(
            raw_prediction["s2"],
            page_id=page_id,
        )
        self.u1 = StringField(
            raw_prediction["u1"],
            page_id=page_id,
        )
        self.u2 = StringField(
            raw_prediction["u2"],
            page_id=page_id,
        )
        self.v7 = StringField(
            raw_prediction["v7"],
            page_id=page_id,
        )
        self.x1 = StringField(
            raw_prediction["x1"],
            page_id=page_id,
        )
        self.y1 = StringField(
            raw_prediction["y1"],
            page_id=page_id,
        )
        self.y2 = StringField(
            raw_prediction["y2"],
            page_id=page_id,
        )
        self.y3 = StringField(
            raw_prediction["y3"],
            page_id=page_id,
        )
        self.y4 = StringField(
            raw_prediction["y4"],
            page_id=page_id,
        )
        self.y5 = StringField(
            raw_prediction["y5"],
            page_id=page_id,
        )
        self.y6 = StringField(
            raw_prediction["y6"],
            page_id=page_id,
        )

    def __str__(self) -> str:
        out_str: str = f":a: {self.a}\n"
        out_str += f":b: {self.b}\n"
        out_str += f":c1: {self.c1}\n"
        out_str += f":c3: {self.c3}\n"
        out_str += f":c41: {self.c41}\n"
        out_str += f":c4a: {self.c4a}\n"
        out_str += f":d1: {self.d1}\n"
        out_str += f":d3: {self.d3}\n"
        out_str += f":e: {self.e}\n"
        out_str += f":f1: {self.f1}\n"
        out_str += f":f2: {self.f2}\n"
        out_str += f":f3: {self.f3}\n"
        out_str += f":g: {self.g}\n"
        out_str += f":g1: {self.g1}\n"
        out_str += f":i: {self.i}\n"
        out_str += f":j: {self.j}\n"
        out_str += f":j1: {self.j1}\n"
        out_str += f":j2: {self.j2}\n"
        out_str += f":j3: {self.j3}\n"
        out_str += f":p1: {self.p1}\n"
        out_str += f":p2: {self.p2}\n"
        out_str += f":p3: {self.p3}\n"
        out_str += f":p6: {self.p6}\n"
        out_str += f":q: {self.q}\n"
        out_str += f":s1: {self.s1}\n"
        out_str += f":s2: {self.s2}\n"
        out_str += f":u1: {self.u1}\n"
        out_str += f":u2: {self.u2}\n"
        out_str += f":v7: {self.v7}\n"
        out_str += f":x1: {self.x1}\n"
        out_str += f":y1: {self.y1}\n"
        out_str += f":y2: {self.y2}\n"
        out_str += f":y3: {self.y3}\n"
        out_str += f":y4: {self.y4}\n"
        out_str += f":y5: {self.y5}\n"
        out_str += f":y6: {self.y6}\n"
        out_str += f":Formula Number: {self.formula_number}\n"
        out_str += f":Owner's First Name: {self.owner_first_name}\n"
        out_str += f":Owner's Surname: {self.owner_surname}\n"
        out_str += f":MRZ Line 1: {self.mrz1}\n"
        out_str += f":MRZ Line 2: {self.mrz2}\n"
        return clean_out_string(out_str)
