"""Test to check if style packages are in same versions as pre-commit config."""

import re
from pathlib import Path

import toml


def _test_version(versions_a, versions_b, key):
    assert versions_a[key].replace("v", "") == versions_b[key].replace("v", "")


def test_style_pkg_versions():
    """Check black, flake8, isort and pydocstyle versions consistency."""
    config = toml.load(Path(__file__).parent.parent.joinpath("pyproject.toml"))
    line_sep = re.compile(r"(==|~=|>=)")
    requirements_versions = {}
    for line in config["project"]["optional-dependencies"]["lint"]:
        split_line = line_sep.split(line.strip())
        requirements_versions[split_line[0]] = split_line[2]

    # Get pre-commit versions
    pre_commit_versions = {}
    pre_commit_path = Path(__file__).parent.parent.joinpath(".pre-commit-config.yaml")
    with open(pre_commit_path, encoding="utf-8") as file_p:
        lines = file_p.readlines()
        for idx, line in enumerate(lines):
            if "repo:" in line:
                pkg_name = line.strip().split("/")[-1].strip().replace("mirrors-", "")
                pkg_version = lines[idx + 1].strip().split(":")[-1].strip()
                pre_commit_versions[pkg_name] = pkg_version

    for req in ("pylint",):
        _test_version(requirements_versions, pre_commit_versions, req)
