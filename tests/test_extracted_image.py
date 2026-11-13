import io
from types import SimpleNamespace

import pytest

import mindee.dependencies.decorators as decorators
import mindee.image.extracted_image as extracted_image_module
from mindee.image.extracted_image import ExtractedImage


class FakeImage:
    def __init__(self, data: bytes):
        self.data = data
        self.format = "PNG"

    def encode(self, image_format: str) -> bytes:
        return image_format.encode()


def _image(filename: str) -> ExtractedImage:
    return ExtractedImage(io.BytesIO(b"image-bytes"), filename, 0, 0)


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        ("crop.jpg", b"JPEG"),
        ("crop.tif", b"TIFF"),
        ("crop.exr", b"OPENEXR"),
        ("crop.pdf", b"PDF"),
        ("crop", b"JPEG"),
    ],
)
def test_write_to_file_infers_format_from_extension(
    monkeypatch, tmp_path, filename: str, expected: bytes
):
    extensions = []

    def format_from_extension(extension: str) -> str:
        extensions.append(extension)
        return expected.decode()

    monkeypatch.setattr(decorators, "requires_bernard", lambda: None)
    monkeypatch.setattr(
        extracted_image_module,
        "bernard_image",
        SimpleNamespace(Image=FakeImage),
    )
    monkeypatch.setattr(
        extracted_image_module,
        "bernard_common",
        SimpleNamespace(format_from_extension=format_from_extension),
    )

    _image(filename).write_to_file(tmp_path)

    assert (tmp_path / filename).read_bytes() == expected
    expected_extension = f".{filename.rsplit('.', 1)[-1]}" if "." in filename else ""
    assert extensions == [expected_extension]


def test_write_to_file_explicit_format_overrides_extension(monkeypatch, tmp_path):
    monkeypatch.setattr(decorators, "requires_bernard", lambda: None)
    monkeypatch.setattr(
        extracted_image_module,
        "bernard_image",
        SimpleNamespace(Image=FakeImage),
    )
    monkeypatch.setattr(
        extracted_image_module,
        "bernard_common",
        SimpleNamespace(
            format_from_extension=lambda extension: pytest.fail(
                "format should not be inferred when explicitly provided"
            )
        ),
    )

    _image("crop.jpg").write_to_file(tmp_path, file_format="PNG")

    assert (tmp_path / "crop.jpg").read_bytes() == b"PNG"


def test_write_to_file_keeps_bytes_when_inferred_format_matches(monkeypatch, tmp_path):
    monkeypatch.setattr(decorators, "requires_bernard", lambda: None)
    monkeypatch.setattr(
        extracted_image_module,
        "bernard_image",
        SimpleNamespace(Image=FakeImage),
    )
    monkeypatch.setattr(
        extracted_image_module,
        "bernard_common",
        SimpleNamespace(format_from_extension=lambda extension: "PNG"),
    )

    _image("crop.png").write_to_file(tmp_path)

    assert (tmp_path / "crop.png").read_bytes() == b"image-bytes"
