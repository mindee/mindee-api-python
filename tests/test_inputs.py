import pytest
from mindee import Inputs


def test_pdf_reconstruct():
    with pytest.raises(Exception):
        Inputs("./tests/data/invoices/invoice_6p.pdf", cut_pdf=True, n_pdf_pages=4)


def test_pdf_reconstruct_check_n_pages():
    input_obj_3 = Inputs(
        "./tests/data/invoices/invoice_6p.pdf", cut_pdf=True, n_pdf_pages=3
    )
    input_obj_2 = Inputs(
        "./tests/data/invoices/invoice_6p.pdf", cut_pdf=True, n_pdf_pages=2
    )
    input_obj_1 = Inputs(
        "./tests/data/invoices/invoice_6p.pdf", cut_pdf=True, n_pdf_pages=1
    )

    # re-initialize file pointer
    input_obj_3.file_object.seek(0)
    input_obj_2.file_object.seek(0)
    input_obj_1.file_object.seek(0)

    assert input_obj_3.count_pdf_pages() == 3
    assert input_obj_2.count_pdf_pages() == 2
    assert input_obj_1.count_pdf_pages() == 1


def test_input_from_stream():
    with open("./tests/data/invoices/invoice_6p.pdf", "rb") as fp:
        input_obj_1 = Inputs(fp, input_type="stream", cut_pdf=True, n_pdf_pages=1)
    assert input_obj_1.count_pdf_pages() == 1


def test_pdf_blank_check():
    with pytest.raises(Exception):
        Inputs("./tests/data/pdfs/blank.pdf")

    with pytest.raises(Exception):
        Inputs("./tests/data/pdfs/blank_1.pdf")

    input_not_blank = Inputs("./tests/data/pdfs/not_blank_image_only.pdf")
    assert input_not_blank.count_pdf_pages() == 1
