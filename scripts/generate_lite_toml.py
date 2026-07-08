from typing import Any

import toml


def generate_lite() -> None:
    """Generates the mindee-lite version of pyproject.toml"""
    with open("pyproject.toml", encoding="utf-8") as file_data:
        data: dict[str, Any] = toml.load(file_data)

    data["project"]["name"] = "mindee-lite"
    data["project"]["description"] = (
        "Mindee API helper library for Python (Lite Version)"
    )

    original_deps = data["project"]["dependencies"]
    heavy_deps = [
        dep for dep in original_deps if str(dep).lower().startswith("bernard-ledit")
    ]
    lite_deps = [
        dep for dep in original_deps if not str(dep).lower().startswith("bernard-ledit")
    ]
    data["project"]["optional-dependencies"]["heavy"] = heavy_deps
    data["project"]["dependencies"] = lite_deps
    data["tool"]["pytest"]["ini_options"]["addopts"] = data["tool"]["pytest"][
        "ini_options"
    ]["addopts"].replace("not lite", "not bernard_ledit")

    with open("pyproject-lite.toml", "w", encoding="utf-8") as file_data:
        toml.dump(data, file_data)

    print("Successfully generated pyproject-lite.toml")


if __name__ == "__main__":
    generate_lite()
