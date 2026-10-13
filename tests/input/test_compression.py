from __future__ import annotations

import os

import pytest

from mindee.input import PathInput
from tests.utils import (
    FILE_TYPES_PATH,
    OUTPUT_PATH,
    V1_PRODUCT_PATH,
    V1_RESOURCE_PATH,
    cleanup_output_files,
)

bernard_ledit = pytest.importorskip("bernard_ledit")

bernard_image = bernard_ledit.image

RECEIPT_PATH = FILE_TYPES_PATH / "receipt.jpg"


def test_image_quality_compress_from_input_source():
    receipt_input = PathInput(RECEIPT_PATH)
    receipt_input.compress(40)

    with open(OUTPUT_PATH / "compress_indirect.jpg", "wb") as f:
        f.write(receipt_input.file_object.read())
        receipt_input.file_object.seek(0)

    initial_file_stats = os.stat(RECEIPT_PATH)
    rendered_file_stats = os.stat(OUTPUT_PATH / "compress_indirect.jpg")
    assert rendered_file_stats.st_size < initial_file_stats.st_size


@pytest.mark.skip("Need to re-render test files.")
def test_image_quality_compresses_from_compressor():
    receipt_inputs = {
        100: PathInput(RECEIPT_PATH),
        75: PathInput(RECEIPT_PATH),
        50: PathInput(RECEIPT_PATH),
        10: PathInput(RECEIPT_PATH),
        1: PathInput(RECEIPT_PATH),
    }
    [value.compress(key) for key, value in receipt_inputs.items()]

    file_names = [
        "compress100.jpg",
        "compress75.jpg",
        "compress50.jpg",
        "compress10.jpg",
        "compress1.jpg",
    ]
    for i, compressed in enumerate(list(receipt_inputs.values())):
        with open(OUTPUT_PATH / file_names[i], "wb") as f:
            f.write(compressed.file_object)

    initial_file_stats = os.stat(RECEIPT_PATH)
    rendered_file_stats = [os.stat(OUTPUT_PATH / file_name) for file_name in file_names]

    assert initial_file_stats.st_size < rendered_file_stats[0].st_size
    assert initial_file_stats.st_size < rendered_file_stats[1].st_size
    assert rendered_file_stats[1].st_size > rendered_file_stats[2].st_size
    assert rendered_file_stats[2].st_size > rendered_file_stats[3].st_size
    assert rendered_file_stats[3].st_size > rendered_file_stats[4].st_size


def test_image_resize_from_input_source():
    image_resize_input = PathInput(RECEIPT_PATH)

    image_resize_input.compress(75, 250, 1000)
    with open(OUTPUT_PATH / "resize_indirect.jpg", "wb") as f:
        f.write(image_resize_input.file_object.read())
        image_resize_input.file_object.seek(0)

    initial_file_stats = os.stat(RECEIPT_PATH)
    rendered_file_stats = os.stat(OUTPUT_PATH / "resize_indirect.jpg")
    assert rendered_file_stats.st_size < initial_file_stats.st_size

    image = bernard_image.Image(image_resize_input.file_object.read())
    assert image.size[0] == 250
    assert image.size[1] == 333


def test_image_resize_from_compressor():
    resizes = [
        PathInput(RECEIPT_PATH),
        PathInput(RECEIPT_PATH),
        PathInput(RECEIPT_PATH),
        PathInput(RECEIPT_PATH),
    ]

    resizes[0].compress(75, 500)
    resizes[1].compress(75, 250, 500)
    resizes[2].compress(75, 500, 250)
    resizes[3].compress(75, None, 250)

    file_names = [
        "resize500xnull.jpg",
        "resize250x500.jpg",
        "resize500x250.jpg",
        "resizenullx250.jpg",
    ]
    for i, resized in enumerate(resizes):
        with open(OUTPUT_PATH / file_names[i], "wb") as f:
            f.write(resized.file_object.read())

    initial_file_stats = os.stat(RECEIPT_PATH)
    rendered_file_stats = [os.stat(OUTPUT_PATH / file_name) for file_name in file_names]

    assert initial_file_stats.st_size > rendered_file_stats[0].st_size
    assert rendered_file_stats[0].st_size > rendered_file_stats[1].st_size
    assert rendered_file_stats[1].st_size > rendered_file_stats[2].st_size
    assert rendered_file_stats[2].st_size == rendered_file_stats[3].st_size


def test_pdf_input_has_text():
    has_source_text_path = FILE_TYPES_PATH / "pdf" / "multipage.pdf"
    has_no_source_text_path = FILE_TYPES_PATH / "pdf" / "blank_1.pdf"
    has_no_source_text_since_its_image_path = RECEIPT_PATH

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
        V1_RESOURCE_PATH / "products" / "invoice_splitter" / "default_sample.pdf"
    )

    pdf_resize_input.compress(75, True)
    with open(OUTPUT_PATH / "resize_indirect.pdf", "wb") as f:
        f.write(pdf_resize_input.file_object.read())

    initial_file_stats = os.stat(
        V1_RESOURCE_PATH / "products/invoice_splitter/default_sample.pdf"
    )
    rendered_file_stats = os.stat(OUTPUT_PATH / "resize_indirect.pdf")

    assert rendered_file_stats.st_size < initial_file_stats.st_size


def test_pdf_compress_from_compressor():
    file_path = (
        V1_RESOURCE_PATH / "products" / "invoice_splitter" / "default_sample.pdf"
    )

    pdf_inputs = {
        85: PathInput(file_path),
        75: PathInput(file_path),
        50: PathInput(file_path),
        10: PathInput(file_path),
    }

    [value.compress(key) for key, value in pdf_inputs.items()]

    file_names = [
        "compress85.pdf",
        "compress75.pdf",
        "compress50.pdf",
        "compress10.pdf",
    ]
    for i, compressed in enumerate(list(pdf_inputs.values())):
        with open(OUTPUT_PATH / file_names[i], "wb") as f:
            f.write(compressed.file_object.read())

    initial_file_stats = os.stat(
        V1_PRODUCT_PATH / "invoice_splitter" / "default_sample.pdf"
    )
    rendered_file_stats = [os.stat(OUTPUT_PATH / file_name) for file_name in file_names]

    assert initial_file_stats.st_size == rendered_file_stats[0].st_size
    assert rendered_file_stats[0].st_size > rendered_file_stats[1].st_size
    assert rendered_file_stats[1].st_size > rendered_file_stats[2].st_size
    assert rendered_file_stats[2].st_size > rendered_file_stats[3].st_size


def test_pdf_compress_with_text_does_not_compress():
    initial_with_text = PathInput(FILE_TYPES_PATH / "pdf" / "multipage.pdf")
    initial_bytes = initial_with_text.file_object.read()
    initial_with_text.file_object.seek(0)

    initial_with_text.compress(50)
    initial_with_text.file_object.seek(0)

    assert initial_with_text.file_object.read() == initial_bytes


@pytest.fixture(scope="module", autouse=True)
def cleanup():
    yield
    cleanup_output_files(
        [
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
    )
