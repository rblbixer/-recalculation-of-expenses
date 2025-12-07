import pytest

from app.bot.handlers.expenses import _parse_add_command


def test_parse_add_command():
    amount, category, description = _parse_add_command("/add 200 food lunch")
    assert amount == 200
    assert category == "food"
    assert description == "lunch"


def test_parse_add_command_invalid():
    with pytest.raises(ValueError):
        _parse_add_command("/add wrong")

