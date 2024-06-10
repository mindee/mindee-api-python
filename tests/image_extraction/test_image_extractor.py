from io import BytesIO

import pypdfium2 as pdfium
import pytest
from PIL import Image

from mindee.error import MimeTypeError
from tests.test_inputs import PRODUCT_DATA_DIR


@pytest.fixture
def single_page_path():
    return PRODUCT_DATA_DIR / "multi_receipts_detector" / "default_sample.jpg"


@pytest.fixture
def multiple_pages_path():
    return PRODUCT_DATA_DIR / "multi_receipts_detector" / "multipage_sample.pdf"


def test_get_images_mono_page(single_page_path):
    with open(single_page_path, "rb") as f:
        jpg_file = Image.open(single_page_path)
    jpg_height = jpg_file.size[0]
    jpg_width = jpg_file.size[1]
    assert jpg_height == 3628
    assert jpg_width == 1552


def test_get_images_multiple_pages(multiple_pages_path):
    with open(multiple_pages_path, "rb") as f:
        pdf = pdfium.PdfDocument(f)
        pdf_images = [page.render().to_pil() for page in pdf]
    height_page_0 = pdf_images[0].size[0]
    width_page_0 = pdf_images[0].size[1]
    assert height_page_0 == 595
    assert width_page_0 == 842

    height_page_1 = pdf_images[1].size[0]
    width_page_1 = pdf_images[1].size[1]
    assert height_page_1 == 595
    assert width_page_1 == 842
