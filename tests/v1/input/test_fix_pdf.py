import pytest

from mindee import PathInput
from mindee.error import MimeTypeError
from tests.utils import FILE_TYPES_DIR


def test_broken_unfixable_pdf():
    with pytest.raises(MimeTypeError):
        input_source = PathInput(FILE_TYPES_DIR / "pdf" / "broken_unfixable.pdf")
        input_source.fix_pdf()


def test_broken_fixable_pdf():
    input_source = PathInput(FILE_TYPES_DIR / "pdf" / "broken_fixable.pdf")
    input_source.fix_pdf()
    assert input_source.page_count == 1


def test_broken_fixable_invoice_pdf():
    input_source = PathInput(FILE_TYPES_DIR / "pdf" / "broken_invoice.pdf")
    input_source.fix_pdf()
