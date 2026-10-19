import pytest

from loader import validate
from exceptions import MissingStartError, InvalidExitError


def make_scenario():
    return {
        "start": "Комната",
        "locations": {
            "Комната": {
                "description": "Маленькая комната",
                "riddle": None,
                "exits": {
                    "север": {
                        "destination": "Коридор",
                        "requires": "Ключ"
                    }
                },
                "items": [
                    {
                        "name": "Ключ",
                        "description": "Старый ключ"
                    }
                ]
            },
            "Коридор": {
                "description": "Длинный коридор",
                "exits": {},
                "items": []
            }
        }
    }


def test_valid_scenario():
    data = make_scenario()
    assert validate(data) is True

def test_missing_start():
    data = make_scenario()
    del data["start"]
    with pytest.raises(MissingStartError):
        validate(data)

def test_invalid_destination():
    data = make_scenario()
    data["locations"]["Комната"]["exits"]["север"] = {"destination": "Подвал"}
    with pytest.raises(InvalidExitError):
        validate(data)

def test_missing_required_item():
    data = make_scenario()
    data["locations"]["Комната"]["exits"]["север"]["requires"] = "Золотой ключ"
    with pytest.raises(InvalidExitError):
        validate(data)

def test_valid_riddle():
    data = make_scenario()
    data["locations"]["Комната"]["riddle"] = {
        "type": "question",
        "question": "Что светит ночью?",
        "answer": "свет",
        "reward": {
            "name": "Карта",
            "description": "Старая карта"
        }
    }
    assert validate(data) is True