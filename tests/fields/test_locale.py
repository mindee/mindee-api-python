from mindee.fields.locale import LocaleField


def test_constructor():
    field_dict = {
        "value": "en-EN",
        "language": "en",
        "country": "uk",
        "currency": "GBP",
        "confidence": 0.1,
    }
    locale = LocaleField(field_dict)
    assert locale.value == "en-EN"
    assert locale.language == "en"
    assert locale.country == "uk"
    assert locale.currency == "GBP"
    assert str(locale) == "en-EN; en; uk; GBP;"


def test_constructor_almost_empty_field():
    field_dict = {"value": "en-EN", "confidence": 0.1}
    locale = LocaleField(field_dict)
    assert locale.language is None
    assert locale.country is None
    assert locale.currency is None


def test_constructor_empty_language():
    field_dict = {
        "value": "en-EN",
        "country": "uk",
        "currency": "GBP",
        "language": "N/A",
        "confidence": 0.1,
    }
    locale = LocaleField(field_dict)
    assert locale.language is None
    assert locale.country == "uk"
    assert locale.currency == "GBP"
    assert str(locale) == "en-EN; uk; GBP;"
