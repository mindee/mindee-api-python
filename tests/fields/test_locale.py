from mindee.fields.locale import Locale


def test_constructor():
    field_dict = {
        "value": "en-EN",
        "language": "en",
        "country": "uk",
        "currency": "GBP",
        "probability": 0.1
    }
    locale = Locale(field_dict)
    assert locale.value == "en-EN"
    assert locale.language == "en"
    assert locale.country == "uk"
    assert locale.currency == "GBP"


def test_constructor_almost_empty_field():
    field_dict = {
        "value": "en-EN",
        "probability": 0.1
    }
    locale = Locale(field_dict)
    assert locale.language is None
    assert locale.country is None
    assert locale.currency is None
