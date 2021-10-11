import pytest
from mindee import Inputs
import fitz


def test_mpdf_reconstruct():
    with pytest.raises(Exception):
        Inputs('./tests/data/invoices/invoice_6p.pdf', cut_pdf=True, n_pdf_pages=4)


def test_mpdf_reconstruct_check_n_pages():
    input_obj_3 = Inputs('./tests/data/invoices/invoice_6p.pdf', cut_pdf=True, n_pdf_pages=3)
    input_obj_2 = Inputs('./tests/data/invoices/invoice_6p.pdf', cut_pdf=True, n_pdf_pages=2)
    input_obj_1 = Inputs('./tests/data/invoices/invoice_6p.pdf', cut_pdf=True, n_pdf_pages=1)
    src_3 = fitz.open(
                stream=input_obj_3.file_object.read(),
                filetype="application/pdf",
                filename="test.pdf"
            )
    src_2 = fitz.open(
                stream=input_obj_2.file_object.read(),
                filetype="application/pdf",
                filename="test.pdf"
            )
    src_1 = fitz.open(
                stream=input_obj_1.file_object.read(),
                filetype="application/pdf",
                filename="test.pdf"
            )
    assert len(src_3) == 3
    assert len(src_2) == 2
    assert len(src_1) == 1
