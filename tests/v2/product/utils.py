from typing import Tuple
from pathlib import Path
import json

from tests.utils import V2_PRODUCT_DATA_DIR


def get_samples(json_path: Path, rst_path: Path) -> Tuple[dict, str]:
    with json_path.open("r", encoding="utf-8") as fh:
        json_sample = json.load(fh)
    try:
        with rst_path.open("r", encoding="utf-8") as fh:
            rst_sample = fh.read()
    except FileNotFoundError:
        rst_sample = ""
    return json_sample, rst_sample


def get_product_samples(product: str, file_name: str) -> Tuple[dict, str]:
    json_path = V2_PRODUCT_DATA_DIR / product / f"{file_name}.json"
    rst_path = V2_PRODUCT_DATA_DIR / product / f"{file_name}.rst"
    return get_samples(json_path, rst_path)
