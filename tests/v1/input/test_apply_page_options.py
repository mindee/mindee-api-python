import io

import pypdfium2 as pdfium
import pytest

from mindee.error import MindeeError
from mindee.input.page_options import KEEP_ONLY, REMOVE, PageOptions
from mindee.input.sources import (
    Base64Input,
    BytesInput,
    FileInput,
    LocalInputSource,
    PathInput,
)
from tests.utils import FILE_TYPES_DIR, V1_PRODUCT_DATA_DIR


def _assert_page_options(input_source: LocalInputSource, numb_pages: int):
    assert input_source.is_pdf() is True
    # Currently the least verbose way of comparing pages with pypdfium2
    # I.e., each page is read and rendered as a rasterized image.
    # These images are then compared as raw byte sequences.
    cut_pdf = pdfium.PdfDocument(input_source.file_object)
    pdf = pdfium.PdfDocument(FILE_TYPES_DIR / "pdf" / f"multipage_cut-{numb_pages}.pdf")
    for idx in range(len(pdf)):
        pdf_page = pdf.get_page(idx)
        pdf_page_render = pdfium.PdfPage.render(pdf_page)
        cut_pdf_page = cut_pdf.get_page(idx)
        cut_pdf_page_render = pdfium.PdfPage.render(cut_pdf_page)

        assert bytes(pdf_page_render.buffer) == bytes(cut_pdf_page_render.buffer)
    cut_pdf.close()
    pdf.close()


def test_pdf_reconstruct_ok():
    input_source = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    input_source.process_pdf(behavior=KEEP_ONLY, on_min_pages=2, page_indexes=range(5))
    assert isinstance(input_source.file_object, io.BytesIO)


@pytest.mark.parametrize("numb_pages", [1, 2, 3])
def test_process_pdf_cut_n_pages(numb_pages: int):
    input_source = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    assert input_source.page_count == 12
    input_source.process_pdf(
        behavior=KEEP_ONLY, on_min_pages=2, page_indexes=[0, -2, -1][:numb_pages]
    )
    assert input_source.page_count == numb_pages
    _assert_page_options(input_source, numb_pages)


@pytest.mark.parametrize("numb_pages", [1, 2, 3])
def test_apply_pages_pdf_cut_n_pages(numb_pages: int):
    input_source = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    assert input_source.page_count == 12
    input_source.apply_page_options(
        PageOptions(on_min_pages=2, page_indexes=[0, -2, -1][:numb_pages])
    )
    assert input_source.page_count == numb_pages
    _assert_page_options(input_source, numb_pages)


def test_pdf_keep_5_first_pages():
    input_source = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    assert input_source.page_count == 12
    input_source.process_pdf(
        behavior=KEEP_ONLY, on_min_pages=2, page_indexes=[0, 1, 2, 3, 4]
    )
    assert input_source.page_count == 5


def test_pdf_keep_invalid_pages():
    input_source = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    assert input_source.page_count == 12
    input_source.process_pdf(
        behavior=KEEP_ONLY, on_min_pages=2, page_indexes=[0, 1, 17]
    )
    assert input_source.page_count == 2


def test_pdf_remove_5_last_pages():
    input_source = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    assert input_source.is_pdf() is True
    input_source.process_pdf(
        behavior=REMOVE, on_min_pages=2, page_indexes=[-5, -4, -3, -2, -1]
    )
    assert input_source.page_count == 7


def test_pdf_remove_5_first_pages():
    input_source = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    assert input_source.is_pdf() is True
    input_source.process_pdf(
        behavior=REMOVE, on_min_pages=2, page_indexes=list(range(5))
    )
    assert input_source.page_count == 7


def test_pdf_remove_invalid_pages():
    input_source = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    assert input_source.is_pdf() is True
    input_source.process_pdf(behavior=REMOVE, on_min_pages=2, page_indexes=[16])
    assert input_source.page_count == 12


def test_pdf_keep_no_pages():
    input_source = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    assert input_source.is_pdf() is True
    # empty page indexes
    with pytest.raises(RuntimeError):
        input_source.process_pdf(behavior=KEEP_ONLY, on_min_pages=2, page_indexes=[])
    # all invalid pages
    with pytest.raises(RuntimeError):
        input_source.process_pdf(
            behavior=KEEP_ONLY, on_min_pages=2, page_indexes=[16, 17]
        )


def test_pdf_remove_all_pages():
    input_source = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    assert input_source.is_pdf() is True
    with pytest.raises(RuntimeError):
        input_source.process_pdf(
            behavior=REMOVE, on_min_pages=2, page_indexes=list(range(15))
        )


def test_pdf_input_from_file():
    with open(FILE_TYPES_DIR / "pdf" / "multipage.pdf", "rb") as fp:
        input_source = FileInput(fp)
        assert input_source.is_pdf() is True
        input_source.process_pdf(behavior=KEEP_ONLY, on_min_pages=2, page_indexes=[0])
    assert input_source.page_count == 1


def test_pdf_input_from_base64():
    with open(V1_PRODUCT_DATA_DIR / "invoices" / "invoice_10p.txt", "rt") as fp:
        input_source = Base64Input(fp.read(), filename="invoice_10p.pdf")
    assert input_source.is_pdf() is True
    input_source.process_pdf(behavior=KEEP_ONLY, on_min_pages=2, page_indexes=[0])
    assert input_source.page_count == 1


def test_pdf_input_from_bytes():
    with open(V1_PRODUCT_DATA_DIR / "invoices" / "invoice_10p.pdf", "rb") as fp:
        input_source = BytesInput(fp.read(), filename="invoice_10p.pdf")
    assert input_source.is_pdf() is True
    input_source.process_pdf(behavior=KEEP_ONLY, on_min_pages=2, page_indexes=[0])
    assert input_source.page_count == 1


def test_pdf_blank_check():
    with pytest.raises(MindeeError):
        input_source = PathInput(FILE_TYPES_DIR / "pdf" / "blank.pdf")
        input_source.process_pdf(behavior=KEEP_ONLY, on_min_pages=2, page_indexes=[0])

    with pytest.raises(MindeeError):
        input_source = PathInput(FILE_TYPES_DIR / "pdf" / "blank_1.pdf")
        input_source.process_pdf(behavior=KEEP_ONLY, on_min_pages=2, page_indexes=[0])

    input_not_blank = PathInput(FILE_TYPES_DIR / "pdf" / "not_blank_image_only.pdf")
    assert input_not_blank.page_count == 1
