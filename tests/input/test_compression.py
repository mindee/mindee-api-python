import operator
import os
from functools import reduce
from pathlib import Path

import pytest
from PIL import Image

from mindee.image_operations.image_compressor import compress_image
from mindee.input.sources.path_input import PathInput
from mindee.pdf.pdf_compressor import compress_pdf
from mindee.pdf.pdf_utils import extract_text_from_pdf

DATA_DIR = Path("./tests/data")
OUTPUT_DIR = DATA_DIR / "output"


def test_image_quality_compress_from_input_source():
    receipt_input = PathInput(DATA_DIR / "file_types/receipt.jpg")
    receipt_input.compress(40)

    with open(OUTPUT_DIR / "compress_indirect.jpg", "wb") as f:
        f.write(receipt_input.file_object.read())
        receipt_input.file_object.seek(0)

    initial_file_stats = os.stat(DATA_DIR / "file_types/receipt.jpg")
    rendered_file_stats = os.stat(OUTPUT_DIR / "compress_indirect.jpg")
    assert rendered_file_stats.st_size < initial_file_stats.st_size


def test_image_quality_compresses_from_compressor():
    receipt_input = PathInput(DATA_DIR / "file_types/receipt.jpg")
    compresses = [
        compress_image(receipt_input.file_object, 100),
        compress_image(receipt_input.file_object),
        compress_image(receipt_input.file_object, 50),
        compress_image(receipt_input.file_object, 10),
        compress_image(receipt_input.file_object, 1),
    ]

    file_names = [
        "compress100.jpg",
        "compress75.jpg",
        "compress50.jpg",
        "compress10.jpg",
        "compress1.jpg",
    ]
    for i, compressed in enumerate(compresses):
        with open(OUTPUT_DIR / file_names[i], "wb") as f:
            f.write(compressed)

    initial_file_stats = os.stat(DATA_DIR / "file_types/receipt.jpg")
    rendered_file_stats = [os.stat(OUTPUT_DIR / file_name) for file_name in file_names]

    assert initial_file_stats.st_size < rendered_file_stats[0].st_size
    assert initial_file_stats.st_size < rendered_file_stats[1].st_size
    assert rendered_file_stats[1].st_size > rendered_file_stats[2].st_size
    assert rendered_file_stats[2].st_size > rendered_file_stats[3].st_size
    assert rendered_file_stats[3].st_size > rendered_file_stats[4].st_size


def test_image_resize_from_input_source():
    image_resize_input = PathInput(DATA_DIR / "file_types/receipt.jpg")

    image_resize_input.compress(75, 250, 1000)
    with open(OUTPUT_DIR / "resize_indirect.jpg", "wb") as f:
        f.write(image_resize_input.file_object.read())
        image_resize_input.file_object.seek(0)

    initial_file_stats = os.stat(DATA_DIR / "file_types/receipt.jpg")
    rendered_file_stats = os.stat(OUTPUT_DIR / "resize_indirect.jpg")
    assert rendered_file_stats.st_size < initial_file_stats.st_size

    image = Image.open(image_resize_input.file_object)
    assert image.width == 250
    assert image.height == 333


def test_image_resize_from_compressor():
    image_resize_input = PathInput(DATA_DIR / "file_types/receipt.jpg")

    resizes = [
        compress_image(image_resize_input.file_object, 75, 500),
        compress_image(image_resize_input.file_object, 75, 250, 500),
        compress_image(image_resize_input.file_object, 75, 500, 250),
        compress_image(image_resize_input.file_object, 75, None, 250),
    ]

    file_names = [
        "resize500xnull.jpg",
        "resize250x500.jpg",
        "resize500x250.jpg",
        "resizenullx250.jpg",
    ]
    for i, resized in enumerate(resizes):
        with open(OUTPUT_DIR / file_names[i], "wb") as f:
            f.write(resized)

    initial_file_stats = os.stat(DATA_DIR / "file_types/receipt.jpg")
    rendered_file_stats = [os.stat(OUTPUT_DIR / file_name) for file_name in file_names]

    assert initial_file_stats.st_size > rendered_file_stats[0].st_size
    assert rendered_file_stats[0].st_size > rendered_file_stats[1].st_size
    assert rendered_file_stats[1].st_size > rendered_file_stats[2].st_size
    assert rendered_file_stats[2].st_size == rendered_file_stats[3].st_size


def test_pdf_input_has_text():
    has_source_text_path = DATA_DIR / "file_types/pdf/multipage.pdf"
    has_no_source_text_path = DATA_DIR / "file_types/pdf/blank_1.pdf"
    has_no_source_text_since_its_image_path = os.path.join(
        DATA_DIR, "file_types/receipt.jpg"
    )

    has_source_text_input = PathInput(has_source_text_path)
    has_no_source_text_input = PathInput(has_no_source_text_path)
    has_no_source_text_since_its_image_input = PathInput(
        has_no_source_text_since_its_image_path
    )

    assert has_source_text_input.has_source_text()
    assert not has_no_source_text_input.has_source_text()
    assert not has_no_source_text_since_its_image_input.has_source_text()


def test_pdf_compress_from_input_source():
    pdf_resize_input = PathInput(
        DATA_DIR / "products/invoice_splitter/default_sample.pdf"
    )

    compressed_pdf = compress_pdf(pdf_resize_input.file_object, 75, True)
    with open(OUTPUT_DIR / "resize_indirect.pdf", "wb") as f:
        f.write(compressed_pdf)

    initial_file_stats = os.stat(
        DATA_DIR / "products/invoice_splitter/default_sample.pdf"
    )
    rendered_file_stats = os.stat(OUTPUT_DIR / "resize_indirect.pdf")

    assert rendered_file_stats.st_size < initial_file_stats.st_size


def test_pdf_compress_from_compressor():
    pdf_resize_input = PathInput(
        DATA_DIR / "products/invoice_splitter/default_sample.pdf"
    )
    resizes = []
    qualities = [85, 75, 50, 10]
    for quality in qualities:
        resizes.append(compress_pdf(pdf_resize_input.file_object, quality))
        pdf_resize_input.file_object.seek(0)

    file_names = [
        "compress85.pdf",
        "compress75.pdf",
        "compress50.pdf",
        "compress10.pdf",
    ]
    for [i, resized] in enumerate(resizes):
        with open(OUTPUT_DIR / file_names[i], "wb") as f:
            f.write(resized)

    initial_file_stats = os.stat(
        DATA_DIR / "products/invoice_splitter/default_sample.pdf"
    )
    rendered_file_stats = [os.stat(OUTPUT_DIR / file_name) for file_name in file_names]

    assert initial_file_stats.st_size > rendered_file_stats[0].st_size
    assert rendered_file_stats[0].st_size > rendered_file_stats[1].st_size
    assert rendered_file_stats[1].st_size > rendered_file_stats[2].st_size
    assert rendered_file_stats[2].st_size > rendered_file_stats[3].st_size


def test_pdf_compress_with_text_keeps_text():
    initial_with_text = PathInput(DATA_DIR / "file_types/pdf/multipage.pdf")

    compressed_with_text = compress_pdf(initial_with_text.file_object, 100, True, False)

    text_chars = []
    for text_info in extract_text_from_pdf(initial_with_text.file_object.read()):
        text_chars.append("".join([ti.char for ti in text_info]))
    initial_with_text.file_object.seek(0)
    original_text = "".join(text_chars)
    compressed_text = "".join(
        [
            text_info.char
            for text_info in reduce(
                operator.concat, extract_text_from_pdf(compressed_with_text)
            )
        ]
    )

    assert compressed_text == original_text


def test_pdf_compress_with_text_does_not_compress():
    initial_with_text = PathInput(DATA_DIR / "file_types/pdf/multipage.pdf")

    compressed_with_text = compress_pdf(initial_with_text.file_object, 50)

    assert compressed_with_text == initial_with_text.file_object.read()


@pytest.fixture(scope="module", autouse=True)
def cleanup():
    yield
    created_files = [
        "compress10.pdf",
        "compress50.pdf",
        "compress75.pdf",
        "compress85.pdf",
        "resize_indirect.pdf",
        "compress1.jpg",
        "compress10.jpg",
        "compress50.jpg",
        "compress75.jpg",
        "compress100.jpg",
        "compress_indirect.jpg",
        "resize250x500.jpg",
        "resize500x250.jpg",
        "resize500xnull.jpg",
        "resize_indirect.jpg",
        "resizenullx250.jpg",
    ]

    for file_path in created_files:
        full_path = DATA_DIR / "output" / file_path
        if full_path.exists():
            os.remove(full_path)
