"""Test to check if style packages are in same versions as pre-commit config."""

import re
from pathlib import Path

import tomli


def _test_version(versions_a, versions_b, key):
    assert versions_a[key].replace("v", "") == versions_b[key].replace("v", "")


def test_style_pkg_versions():
    """Check black, flake8, isort and pydocstyle versions consistency."""
    config = tomli.loads(
        Path(__file__).parent.parent.joinpath("pyproject.toml").read_text()
    )
    line_sep = re.compile(r"(==|~=|>=)")
    requirements_versions = {}
    for line in config["project"]["optional-dependencies"]["lint"]:
        split_line = line_sep.split(line.strip())
        requirements_versions[split_line[0]] = split_line[2]

    # Get pre-commit versions
    pre_commit_versions = {}
    config = tomli.loads(Path(__file__).parent.parent.joinpath("prek.toml").read_text())
    for repo in config["repos"]:
        if not repo.get("rev"):
            continue
        pkg_name = repo["repo"].strip().split("/")[-1].strip().replace("mirrors-", "")
        pkg_version = repo["rev"].strip().split(":")[-1].strip()
        pre_commit_versions[pkg_name] = pkg_version

    for req in ("pylint",):
        _test_version(requirements_versions, pre_commit_versions, req)
