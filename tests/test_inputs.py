import io

import pytest
from mindee.inputs import PathDocument, FileDocument, BytesDocument, Base64Document


def test_pdf_reconstruct_fail():
    with pytest.raises(AssertionError):
        PathDocument(
            "./tests/data/invoices/invoice_6p.pdf",
            cut_pdf=True,
            n_pdf_pages=4,
        )


def test_pdf_reconstruct_ok():
    input_file = PathDocument("./tests/data/invoices/invoice_6p.pdf")
    assert isinstance(input_file.file_object, io.BytesIO)


def test_pdf_reconstruct_check_n_pages():
    input_obj_3 = PathDocument(
        "./tests/data/invoices/invoice_6p.pdf",
        cut_pdf=True,
        n_pdf_pages=3,
    )
    input_obj_2 = PathDocument(
        "./tests/data/invoices/invoice_6p.pdf",
        cut_pdf=True,
        n_pdf_pages=2,
    )
    input_obj_1 = PathDocument(
        "./tests/data/invoices/invoice_6p.pdf",
        cut_pdf=True,
        n_pdf_pages=1,
    )

    # re-initialize file pointer
    input_obj_3.file_object.seek(0)
    input_obj_2.file_object.seek(0)
    input_obj_1.file_object.seek(0)

    assert input_obj_3.count_pdf_pages() == 3
    assert input_obj_2.count_pdf_pages() == 2
    assert input_obj_1.count_pdf_pages() == 1


def test_input_from_path():
    input_obj_1 = PathDocument(
        "./tests/data/invoices/invoice_6p.pdf",
        cut_pdf=True,
        n_pdf_pages=1,
    )
    assert input_obj_1.count_pdf_pages() == 1


def test_input_from_file():
    with open("./tests/data/invoices/invoice_6p.pdf", "rb") as fp:
        input_obj_1 = FileDocument(fp, cut_pdf=True, n_pdf_pages=1)
    assert input_obj_1.count_pdf_pages() == 1


def test_input_from_base64():
    with open("./tests/data/invoices/invoice_6p.txt", "rt") as fp:
        input_obj_1 = Base64Document(
            fp.read(),
            filename="invoice_6p.pdf",
            cut_pdf=True,
            n_pdf_pages=1,
        )
    assert input_obj_1.count_pdf_pages() == 1


def test_input_from_bytes():
    with open("./tests/data/invoices/invoice_6p.pdf", "rb") as fp:
        input_obj_1 = BytesDocument(
            fp.read(),
            filename="invoice_6p.pdf",
            cut_pdf=True,
            n_pdf_pages=1,
        )
    assert input_obj_1.count_pdf_pages() == 1


def test_pdf_blank_check():
    with pytest.raises(Exception):
        PathDocument("./tests/data/pdfs/blank.pdf")

    with pytest.raises(Exception):
        PathDocument("./tests/data/pdfs/blank_1.pdf")

    input_not_blank = PathDocument("./tests/data/pdfs/not_blank_image_only.pdf")
    assert input_not_blank.count_pdf_pages() == 1
