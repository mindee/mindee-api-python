from typing import Any

import tomli
import tomli_w


def generate_lite() -> None:
    """Generates the mindee-lite version of pyproject.toml"""
    with open("pyproject.toml", encoding="utf-8") as read_handle:
        data: dict[str, Any] = tomli.loads(read_handle.read())

    data["project"]["name"] = "mindee-lite"
    data["project"]["description"] = (
        "Mindee API helper library for Python (Lite Version)"
    )

    original_deps = data["project"]["dependencies"]
    heavy_deps = [
        dep
        for dep in original_deps
        if str(dep).lower().startswith("pillow")
        or str(dep).lower().startswith("pypdfium2")
    ]
    lite_deps = [
        dep
        for dep in original_deps
        if not str(dep).lower().startswith("pillow")
        and not str(dep).lower().startswith("pypdfium2")
    ]
    data["project"]["optional-dependencies"]["heavy"] = heavy_deps
    data["project"]["dependencies"] = lite_deps
    data["tool"]["pytest"]["ini_options"]["addopts"] = data["tool"]["pytest"][
        "ini_options"
    ]["addopts"].replace(" lite", " pypdfium2 and not pillow")

    with open("pyproject-lite.toml", "w", encoding="utf-8") as write_handle:
        write_handle.write(tomli_w.dumps(data))

    print("Successfully generated pyproject-lite.toml")


if __name__ == "__main__":
    generate_lite()
