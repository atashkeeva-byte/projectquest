import json
import pytest

from classes import Game, Location, Item
from saving import save_game, load_save
from exceptions import InvalidLoadError, InvalidLoadItemError

def create_game():
    room = Location("Комната", "Небольшая комната")
    corridor = Location("Коридор", "Длинный коридор")
    key = Item("Ключ", "Старый железный ключ")
    room.add_item(key)
    locations = {
        "Комната": room,
        "Коридор": corridor,
    }
    return Game(locations, "Комната", "Имя")

def test_save_game(tmp_path):
    game = create_game()
    save_file = tmp_path / "save.json"
    save_game(game, str(save_file))
    with open(save_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    assert data["player_name"] == "Имя"
    assert data["current_location"] == "Комната"
    assert data["inventory"] == []
    assert data["location_items"]["Комната"] == ["Ключ"]

def test_load_save(tmp_path):
    original_game = create_game()
    key = original_game.player.current_location.items[0]
    original_game.player.take_item(key)
    original_game.player.current_location = original_game.locations["Коридор"]
    save_file = tmp_path / "save.json"
    save_game(original_game, str(save_file))
    new_game = create_game()
    result = load_save(new_game, str(save_file))
    assert result is True
    assert new_game.player.current_location.name == "Коридор"
    assert [item.name for item in new_game.player.inventory] == ["Ключ"]
    assert new_game.locations["Комната"].items == []

def test_load_missing_file(tmp_path):
    game = create_game()
    save_file = tmp_path / "missing.json"
    with pytest.raises(InvalidLoadError):
        load_save(game, str(save_file))

def test_load_incomplete_save(tmp_path):
    game = create_game()
    save_file = tmp_path / "save.json"
    save_file.write_text('{"player_name": "Имя"}', encoding="utf-8")
    try:
        load_save(game, str(save_file))
    except InvalidLoadError:
        pass
    else:
        assert False

def test_failed_load_does_not_change_game(tmp_path):
    game = create_game()
    original_location = game.player.current_location
    original_items = list(original_location.items)
    save_file = tmp_path / "save.json"
    save_file.write_text(
        """
        {
            "player_name": "Имя",
            "current_location": "Коридор",
            "inventory": ["Несуществующий предмет"],
            "location_items": {
                "Комната": ["Ключ"],
                "Коридор": []
            }
        }
        """,
        encoding="utf-8"
    )
    with pytest.raises(InvalidLoadItemError):
        load_save(game, str(save_file))

    assert game.player.current_location is original_location
    assert game.player.inventory == []
    assert game.locations["Комната"].items == original_items