from pathlib import Path

PRODUCT_DATA_DIR = Path("./tests/data/products/")


def get_version(rst_str: str) -> str:
    """Replaces the version of a created object to avoid errors during tests."""

    version_line_start_pos = rst_str.find(":Product: ")
    version_end_pos = rst_str.find("\n", version_line_start_pos)
    version_start_pos = rst_str.rfind(" v", version_line_start_pos, version_end_pos)
    return rst_str[version_start_pos + 2 : version_end_pos]


def get_id(rst_str: str) -> str:
    """Replaces the string of a created object to avoid errors during tests."""
    id_end_pos = rst_str.find("\n:Filename:")
    id_start_pos = rst_str.find(":Mindee ID: ")
    return rst_str[id_start_pos + 12 : id_end_pos]
