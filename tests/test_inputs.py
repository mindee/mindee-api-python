import io
from pathlib import Path

import pikepdf
import pytest

from mindee.error.mimetype_error import MimeTypeError
from mindee.error.mindee_error import MindeeError, MindeeSourceError
from mindee.input.page_options import KEEP_ONLY, REMOVE
from mindee.input.sources import (
    Base64Input,
    BytesInput,
    FileInput,
    PathInput,
    UrlInputSource,
)
from tests.product import PRODUCT_DATA_DIR

FILE_TYPES_DIR = Path("./tests/data/file_types")

#
# PDF
#


def test_pdf_reconstruct_ok():
    input_obj = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    input_obj.process_pdf(behavior=KEEP_ONLY, on_min_pages=2, page_indexes=range(5))
    assert isinstance(input_obj.file_object, io.BytesIO)


def test_pdf_read_contents():
    input_doc = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    contents = input_doc.read_contents(close_file=False)
    assert contents[0] == "multipage.pdf"
    assert isinstance(contents[1], bytes)
    assert not input_doc.file_object.closed

    input_doc.read_contents(close_file=True)
    assert input_doc.file_object.closed


def test_pdf_reconstruct_no_cut():
    input_file = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    assert input_file.count_doc_pages() == 12
    assert isinstance(input_file.file_object, io.BufferedReader)


@pytest.mark.parametrize("numb_pages", [1, 2, 3])
def test_pdf_cut_n_pages(numb_pages: int):
    input_obj = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    assert input_obj.is_pdf() is True
    input_obj.process_pdf(
        behavior=KEEP_ONLY, on_min_pages=2, page_indexes=[0, -2, -1][:numb_pages]
    )
    assert input_obj.count_doc_pages() == numb_pages

    # Each page in the PDF has a unique (and increasing) /Content /Length.
    # We use this to make sure we have the correct pages
    cut_pdf = pikepdf.open(input_obj.file_object)
    with pikepdf.open(
        FILE_TYPES_DIR / "pdf" / f"multipage_cut-{numb_pages}.pdf"
    ) as pdf:
        for idx, page in enumerate(pdf.pages):
            assert (
                page["/Contents"]["/Length"]
                == cut_pdf.pages[idx]["/Contents"]["/Length"]
            )
    cut_pdf.close()


def test_pdf_keep_5_first_pages():
    input_obj = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    assert input_obj.is_pdf() is True
    input_obj.process_pdf(
        behavior=KEEP_ONLY, on_min_pages=2, page_indexes=[0, 1, 2, 3, 4]
    )
    assert input_obj.count_doc_pages() == 5


def test_pdf_keep_invalid_pages():
    input_obj = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    assert input_obj.is_pdf() is True
    input_obj.process_pdf(behavior=KEEP_ONLY, on_min_pages=2, page_indexes=[0, 1, 17])
    assert input_obj.count_doc_pages() == 2


def test_pdf_remove_5_last_pages():
    input_obj = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    assert input_obj.is_pdf() is True
    input_obj.process_pdf(
        behavior=REMOVE, on_min_pages=2, page_indexes=[-5, -4, -3, -2, -1]
    )
    assert input_obj.count_doc_pages() == 7


def test_pdf_remove_5_first_pages():
    input_obj = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    assert input_obj.is_pdf() is True
    input_obj.process_pdf(behavior=REMOVE, on_min_pages=2, page_indexes=list(range(5)))
    assert input_obj.count_doc_pages() == 7


def test_pdf_remove_invalid_pages():
    input_obj = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    assert input_obj.is_pdf() is True
    input_obj.process_pdf(behavior=REMOVE, on_min_pages=2, page_indexes=[16])
    assert input_obj.count_doc_pages() == 12


def test_pdf_keep_no_pages():
    input_obj = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    assert input_obj.is_pdf() is True
    # empty page indexes
    with pytest.raises(RuntimeError):
        input_obj.process_pdf(behavior=KEEP_ONLY, on_min_pages=2, page_indexes=[])
    # all invalid pages
    with pytest.raises(RuntimeError):
        input_obj.process_pdf(behavior=KEEP_ONLY, on_min_pages=2, page_indexes=[16, 17])


def test_pdf_remove_all_pages():
    input_obj = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    assert input_obj.is_pdf() is True
    with pytest.raises(RuntimeError):
        input_obj.process_pdf(
            behavior=REMOVE, on_min_pages=2, page_indexes=list(range(15))
        )


def test_pdf_input_from_file():
    with open(FILE_TYPES_DIR / "pdf" / "multipage.pdf", "rb") as fp:
        input_obj = FileInput(fp)
        assert input_obj.is_pdf() is True
        input_obj.process_pdf(behavior=KEEP_ONLY, on_min_pages=2, page_indexes=[0])
    assert input_obj.count_doc_pages() == 1


def test_pdf_input_from_base64():
    with open(PRODUCT_DATA_DIR / "invoices" / "invoice_10p.txt", "rt") as fp:
        input_obj = Base64Input(fp.read(), filename="invoice_10p.pdf")
    assert input_obj.is_pdf() is True
    input_obj.process_pdf(behavior=KEEP_ONLY, on_min_pages=2, page_indexes=[0])
    assert input_obj.count_doc_pages() == 1


def test_pdf_input_from_bytes():
    with open(PRODUCT_DATA_DIR / "invoices" / "invoice_10p.pdf", "rb") as fp:
        input_obj = BytesInput(fp.read(), filename="invoice_10p.pdf")
    assert input_obj.is_pdf() is True
    input_obj.process_pdf(behavior=KEEP_ONLY, on_min_pages=2, page_indexes=[0])
    assert input_obj.count_doc_pages() == 1


def test_pdf_input_from_url():
    with pytest.raises(MindeeSourceError):
        UrlInputSource(url="http://example.com/invoice.pdf")


def test_pdf_blank_check():
    with pytest.raises(MindeeError):
        input_obj = PathInput(FILE_TYPES_DIR / "pdf" / "blank.pdf")
        input_obj.process_pdf(behavior=KEEP_ONLY, on_min_pages=2, page_indexes=[0])

    with pytest.raises(MindeeError):
        input_obj = PathInput(FILE_TYPES_DIR / "pdf" / "blank_1.pdf")
        input_obj.process_pdf(behavior=KEEP_ONLY, on_min_pages=2, page_indexes=[0])

    input_not_blank = PathInput(FILE_TYPES_DIR / "pdf" / "not_blank_image_only.pdf")
    assert input_not_blank.count_doc_pages() == 1


#
# Images
#


def test_tif_input_from_path():
    input_obj_1 = PathInput(FILE_TYPES_DIR / "receipt.tif")
    assert input_obj_1.file_mimetype == "image/tiff"

    input_obj_2 = PathInput(FILE_TYPES_DIR / "receipt.tiff")
    assert input_obj_2.file_mimetype == "image/tiff"


def test_heic_input_from_path():
    input_obj_1 = PathInput(FILE_TYPES_DIR / "receipt.heic")
    assert input_obj_1.file_mimetype == "image/heic"


def test_txt_input_from_path():
    with pytest.raises(MimeTypeError):
        PathInput(FILE_TYPES_DIR / "receipt.txt")
