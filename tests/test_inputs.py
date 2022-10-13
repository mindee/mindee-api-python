import io

import pikepdf
import pytest

from mindee.inputs import Base64Document, BytesDocument, FileDocument, PathDocument
from tests import INVOICE_DATA_DIR, PDF_DATA_DIR, RECEIPT_DATA_DIR

#
# PDF
#


def test_pdf_reconstruct_fail():
    with pytest.raises(AssertionError):
        input_obj = PathDocument(f"{INVOICE_DATA_DIR}/invoice_10p.pdf")
        input_obj.process_pdf(num_pdf_pages=4)


def test_pdf_reconstruct_ok():
    input_obj = PathDocument(f"{INVOICE_DATA_DIR}/invoice_10p.pdf")
    input_obj.process_pdf(num_pdf_pages=2)
    assert isinstance(input_obj.file_object, io.BytesIO)


def test_pdf_read_contents():
    input_doc = PathDocument(f"{INVOICE_DATA_DIR}/invoice.pdf")
    contents = input_doc.read_contents(close_file=False)
    assert contents[0] == "invoice.pdf"
    assert isinstance(contents[1], bytes)
    assert not input_doc.file_object.closed

    input_doc.read_contents(close_file=True)
    assert input_doc.file_object.closed


def test_pdf_reconstruct_no_cut():
    input_file = PathDocument(f"{INVOICE_DATA_DIR}/invoice_10p.pdf")
    assert input_file.count_pdf_pages() == 10
    assert isinstance(input_file.file_object, io.BufferedReader)


@pytest.mark.parametrize("numb_pages", [1, 2, 3])
def test_pdf_cut_n_pages(numb_pages: int):
    input_obj = PathDocument(f"{PDF_DATA_DIR}/multipage.pdf")
    assert input_obj.is_pdf() is True
    input_obj.process_pdf(num_pdf_pages=numb_pages)
    assert input_obj.count_pdf_pages() == numb_pages

    # Each page in the PDF has a unique (and increasing) /Content /Length.
    # We use this to make sure we have the correct pages
    cut_pdf = pikepdf.open(input_obj.file_object)
    with pikepdf.open(f"{PDF_DATA_DIR}/multipage_cut-{numb_pages}.pdf") as pdf:
        for idx, page in enumerate(pdf.pages):
            assert (
                page["/Contents"]["/Length"]
                == cut_pdf.pages[idx]["/Contents"]["/Length"]
            )
    cut_pdf.close()


def test_pdf_specify_pages():
    input_obj = PathDocument(f"{PDF_DATA_DIR}/multipage.pdf")
    assert input_obj.is_pdf() is True
    input_obj.process_pdf(pdf_pages_list=[0, 1, 2, 3, 4])
    assert input_obj.count_pdf_pages() == 5


def test_pdf_input_from_path():
    input_obj = PathDocument(f"{INVOICE_DATA_DIR}/invoice_10p.pdf")
    assert input_obj.is_pdf() is True
    input_obj.process_pdf(num_pdf_pages=1)
    assert input_obj.count_pdf_pages() == 1


def test_pdf_input_from_file():
    with open(f"{INVOICE_DATA_DIR}/invoice_10p.pdf", "rb") as fp:
        input_obj = FileDocument(fp)
        assert input_obj.is_pdf() is True
        input_obj.process_pdf(num_pdf_pages=1)
    assert input_obj.count_pdf_pages() == 1


def test_pdf_input_from_base64():
    with open(f"{INVOICE_DATA_DIR}/invoice_10p.txt", "rt") as fp:
        input_obj = Base64Document(fp.read(), filename="invoice_10p.pdf")
    assert input_obj.is_pdf() is True
    input_obj.process_pdf(num_pdf_pages=1)
    assert input_obj.count_pdf_pages() == 1


def test_pdf_input_from_bytes():
    with open(f"{INVOICE_DATA_DIR}/invoice_10p.pdf", "rb") as fp:
        input_obj = BytesDocument(fp.read(), filename="invoice_10p.pdf")
    assert input_obj.is_pdf() is True
    input_obj.process_pdf(num_pdf_pages=1)
    assert input_obj.count_pdf_pages() == 1


def test_pdf_blank_check():
    with pytest.raises(AssertionError):
        input_obj = PathDocument(f"{PDF_DATA_DIR}/blank.pdf")
        input_obj.process_pdf(num_pdf_pages=3)

    with pytest.raises(AssertionError):
        input_obj = PathDocument(f"{PDF_DATA_DIR}/blank_1.pdf")
        input_obj.process_pdf(num_pdf_pages=3)

    input_not_blank = PathDocument(f"{PDF_DATA_DIR}/not_blank_image_only.pdf")
    assert input_not_blank.count_pdf_pages() == 1


#
# Images
#


def test_tif_input_from_path():
    input_obj_1 = PathDocument(f"{RECEIPT_DATA_DIR}/receipt.tif")
    assert input_obj_1.file_mimetype == "image/tiff"

    input_obj_2 = PathDocument(f"{RECEIPT_DATA_DIR}/receipt.tiff")
    assert input_obj_2.file_mimetype == "image/tiff"


def test_heic_input_from_path():
    input_obj_1 = PathDocument(f"{RECEIPT_DATA_DIR}/receipt.heic")
    assert input_obj_1.file_mimetype == "image/heic"
