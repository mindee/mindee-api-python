from pathlib import Path

from mindee.mindee_http.mindee_api import (
    API_KEY_ENV_NAME,
    BASE_URL_ENV_NAME,
    REQUEST_TIMEOUT_ENV_NAME,
)


def clear_envvars(monkeypatch) -> None:
    """
    If we have envvars set, the test will pick them up and fail,
    so let's make sure they're empty.
    """
    monkeypatch.setenv(API_KEY_ENV_NAME, "")
    monkeypatch.setenv(BASE_URL_ENV_NAME, "")
    monkeypatch.setenv(REQUEST_TIMEOUT_ENV_NAME, "")


def dummy_envvars(monkeypatch) -> None:
    """
    Set all API keys to 'dummy'.
    """
    monkeypatch.setenv(API_KEY_ENV_NAME, "dummy")


EXTRAS_DIR = Path("./tests/data/extras/")


def levenshtein_distance(reference_str: str, target_str: str) -> int:
    """
    Calculate the Levenshtein distance between two strings.

    The Levenshtein distance is a measure of the difference between two sequences.
    Informally, the Levenshtein distance between two words is the minimum number
    of single-character edits (insertions, deletions or substitutions) required
    to change one word into the other.


    :param reference_str: The reference string.
    :param target_str: The target string.

    :return: The distance between the two strings.
    """
    reference_len, target_len = len(reference_str), len(target_str)
    previous_row = list(range(target_len + 1))
    current_row = [0] * (target_len + 1)

    for i in range(reference_len):
        current_row[0] = i + 1

        for j in range(target_len):
            deletion_cost = previous_row[j + 1] + 1
            insertion_cost = current_row[j] + 1
            substitution_cost = previous_row[j] if reference_str[i] == target_str[j] else previous_row[j] + 1

            current_row[j + 1] = min(deletion_cost, insertion_cost, substitution_cost)

        previous_row, current_row = current_row, previous_row

    return previous_row[target_len]


def levenshtein_ratio(ref_str: str, target_str: str) -> float:
    """
    Calculates the Levenshtein ratio between two strings.

    :param ref_str: Reference string.
    :param target_str: Target String.
    :return: Ratio between the two strings
    """
    lev_distance = levenshtein_distance(ref_str, target_str)
    max_len = max(len(ref_str), len(target_str))

    if max_len == 0:
        return 1.0

    return 1.0 - (lev_distance / max_len)
