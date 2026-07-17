import pytest

from mindee.v2.parsing.inference.field.simple_field import SimpleField


def _make_field(value) -> SimpleField:
    return SimpleField({"value": value} if value is not None else {})


@pytest.mark.v2
class TestSimpleFieldStringValue:
    def test_returns_string_when_value_is_string(self):
        field = _make_field("hello")
        assert field.string_value == "hello"

    def test_returns_none_when_value_is_none(self):
        field = _make_field(None)
        assert field.string_value is None

    def test_raises_when_value_is_number(self):
        field = _make_field(3.14)
        with pytest.raises(ValueError, match="Value is not a string"):
            _ = field.string_value

    def test_raises_when_value_is_boolean(self):
        field = _make_field(True)
        with pytest.raises(ValueError, match="Value is not a string"):
            _ = field.string_value


@pytest.mark.v2
class TestSimpleFieldNumberValue:
    def test_returns_float_when_value_is_float(self):
        field = _make_field(3.14)
        assert field.number_value == 3.14

    def test_returns_float_when_value_is_int(self):
        # Integers are coerced to float in the constructor
        field = SimpleField({"value": 42})
        assert field.number_value == 42.0
        assert isinstance(field.number_value, float)

    def test_returns_none_when_value_is_none(self):
        field = _make_field(None)
        assert field.number_value is None

    def test_raises_when_value_is_string(self):
        field = _make_field("42")
        with pytest.raises(ValueError, match="Value is not a number"):
            _ = field.number_value

    def test_raises_when_value_is_boolean(self):
        field = _make_field(True)
        with pytest.raises(ValueError, match="Value is not a number"):
            _ = field.number_value


@pytest.mark.v2
class TestSimpleFieldBooleanValue:
    def test_returns_true_when_value_is_true(self):
        field = _make_field(True)
        assert field.boolean_value is True

    def test_returns_false_when_value_is_false(self):
        field = _make_field(False)
        assert field.boolean_value is False

    def test_returns_none_when_value_is_none(self):
        field = _make_field(None)
        assert field.boolean_value is None

    def test_raises_when_value_is_string(self):
        field = _make_field("true")
        with pytest.raises(ValueError, match="Value is not a boolean"):
            _ = field.boolean_value

    def test_raises_when_value_is_number(self):
        field = _make_field(1.0)
        with pytest.raises(ValueError, match="Value is not a boolean"):
            _ = field.boolean_value
