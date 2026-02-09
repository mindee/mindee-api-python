import pytest

from mindee import LocalResponse
from mindee.v2.product.ocr.ocr_page import OCRPage
from mindee.v2.product.ocr import OCRInference
from mindee.v2.product.ocr.ocr_response import OCRResponse
from mindee.v2.product.ocr.ocr_result import OCRResult
from tests.utils import V2_PRODUCT_DATA_DIR


@pytest.mark.v2
def test_ocr_single():
    input_inference = LocalResponse(V2_PRODUCT_DATA_DIR / "ocr" / "ocr_single.json")
    ocr_response = input_inference.deserialize_response(OCRResponse)
    assert isinstance(ocr_response.inference, OCRInference)
    assert ocr_response.inference.result.pages
    assert len(ocr_response.inference.result.pages) == 1
    assert ocr_response.inference.result.pages[0].words[0].content == "Shipper:"
    assert (
        ocr_response.inference.result.pages[0].words[0].polygon[0][0]
        == 0.09742441209406495
    )
    assert (
        ocr_response.inference.result.pages[0].words[0].polygon[0][1]
        == 0.07007125890736342
    )
    assert (
        ocr_response.inference.result.pages[0].words[0].polygon[1][0]
        == 0.15621500559910415
    )
    assert (
        ocr_response.inference.result.pages[0].words[0].polygon[1][1]
        == 0.07046714172604909
    )
    assert (
        ocr_response.inference.result.pages[0].words[0].polygon[2][0]
        == 0.15621500559910415
    )
    assert (
        ocr_response.inference.result.pages[0].words[0].polygon[2][1]
        == 0.08155186064924783
    )
    assert (
        ocr_response.inference.result.pages[0].words[0].polygon[3][0]
        == 0.09742441209406495
    )
    assert (
        ocr_response.inference.result.pages[0].words[0].polygon[3][1]
        == 0.08155186064924783
    )
    assert len(ocr_response.inference.result.pages[0].words) == 305
    assert ocr_response.inference.result.pages[0].content == (
        "Shipper: GLOBAL FREIGHT SOLUTIONS INC. 123 OCEAN DRIVE SHANGHAI, CHINA TEL: "
        "86-21-12345678 FAX: 86-21-87654321\nConsignee: PACIFIC TRADING CO. 789 TRADE "
        "STREET SINGAPORE 567890 SINGAPORE TEL: 65-65432100 FAX: 65-65432101\nNotify "
        "Party (Complete name and address): SAME AS CONSIGNEE\nBILL OF LADING\nJob No "
        ".: XYZ123456\nGLOBAL SHIPPING CO\nPlace of receipt:\nSHANGHAI, CHINA\nOcean "
        "vessel:\nGLOBAL VOYAGER V-202\nPort of loading:\nSHANGHAI, CHINA\nPort of "
        "discharge:\nLOS ANGELES, USA\nPlace of delivery:\nLOS ANGELES, USA\nMarks and "
        "numbers:\nP+F\n(IN DIA.)\nP/N: 12345\nDRAWING NO. A1B2C3\nNumber and kinds of "
        "packages: 1CTN ELECTRONIC COMPONENTS 50 PCS\nDescription of goods:\nGross "
        "weight:\n500 KGS\nMeasurement:\n1.5 M3\nP/O: 987654 LOT NO. "
        "112233\nFFAU1234567/40'HQ/CFS-CFS ICTN/500KGS/1.5M3 SEAL NO:ABC1234567\nMADE "
        'IN CHINA\nSAY TOTAL:\n2 PLTS ONLY\n"FREIGHT COLLECT" CFS-CFS\n** SURRENDERED '
        "**\nFreight and Charge\nOCEAN FREIGHT\nRevenue tons\nRate\nPrepaid\nCollect\n"
        "AS ARRANGED\nThe goods and instructions are accepted and dealt with subject "
        "to the Standard Conditions printed overleaf. Taken in charge in apparent good "
        "order and condition, unless otherwise noted herein, at the place of receipt "
        "for transport and delivery as mentioned above. One of these Combined "
        "Transport Bills of Lading must be surrendered duly endorsed in exchange for "
        "the goods. In Witness whereof the original Combined Transport Bills of Lading "
        "all of this tenor and date have been signed in the number stated below, one "
        "of which being accomplished the other(s) to be void.\nUSD: 31.57 SHIPPED ON "
        "BOARD: 30. SEP. 2022\nFreight Amount OCEAN FREIGHT\nFreight payable at\n"
        "DESTINATION\nNumber of original\nZERO (0)\nCargo insurance\nnot covered\n"
        "Covered according to attached Policy\nPlace and date of issue\nTAIPEI, "
        "TAIWAN: 30. SEP. 2022\nFor delivery of goods please apply to: INTERNATIONAL "
        "LOGISTICS LTD 456 SHIPPING LANE LOS ANGELES, CA 90001 USA TEL:1-213-9876543 "
        "FAX:1-213-9876544 ATTN: MR. JOHN DOE\nSignature: GLOBAL SHIPPING CO., "
        "LTD.\nBY\nAS CARRIER"
    )


@pytest.mark.v2
def test_ocr_multiple():
    input_inference = LocalResponse(V2_PRODUCT_DATA_DIR / "ocr" / "ocr_multiple.json")
    ocr_response = input_inference.deserialize_response(OCRResponse)
    assert isinstance(ocr_response.inference, OCRInference)
    assert isinstance(ocr_response.inference.result, OCRResult)
    assert isinstance(ocr_response.inference.result.pages[0], OCRPage)
    assert len(ocr_response.inference.result.pages) == 3

    assert len(ocr_response.inference.result.pages[0].words) == 295
    assert ocr_response.inference.result.pages[0].words[0].content == "FICTIOCORP"
    assert (
        ocr_response.inference.result.pages[0].words[0].polygon[0][0]
        == 0.06649402824332337
    )
    assert (
        ocr_response.inference.result.pages[0].words[0].polygon[0][1]
        == 0.03957449719523875
    )
    assert (
        ocr_response.inference.result.pages[0].words[0].polygon[1][0]
        == 0.23219061218068954
    )
    assert (
        ocr_response.inference.result.pages[0].words[0].polygon[1][1]
        == 0.03960015049938432
    )
    assert (
        ocr_response.inference.result.pages[0].words[0].polygon[2][0]
        == 0.23219061218068954
    )
    assert (
        ocr_response.inference.result.pages[0].words[0].polygon[2][1]
        == 0.06770762074155151
    )
    assert (
        ocr_response.inference.result.pages[0].words[0].polygon[3][0]
        == 0.06649402824332337
    )
    assert (
        ocr_response.inference.result.pages[0].words[0].polygon[3][1]
        == 0.06770762074155151
    )

    assert len(ocr_response.inference.result.pages[1].words) == 450
    assert ocr_response.inference.result.pages[1].words[0].content == "KEOLIO"

    assert len(ocr_response.inference.result.pages[2].words) == 355
    assert ocr_response.inference.result.pages[2].words[0].content == "KEOLIO"
