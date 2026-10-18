import json
from exceptions import SaveError, InvalidSaveError, LoadError, InvalidLoadError, InvalidLoadLocationError, InvalidLoadItemError, InvalidNameError


def save_game(game, filename: str = "data/save.json") -> None:
    data = {
        "player_name": game.player.name,
        "current_location": game.player.current_location.name,
        "inventory": [item.name for item in game.player.inventory],
        "location_items": {
            location.name: [item.name for item in location.items] for location in game.locations.values()
        },
    }
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)
    except OSError:
        raise InvalidSaveError("Not able to save")
    print("Game saved")

def load_save(game, filename: str = "data/save.json") -> bool:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        raise InvalidLoadError("Not able to read")

    if not isinstance(data, dict):
        raise InvalidLoadError("Save must contain a JSON object")

    required_keys = {
        "player_name",
        "current_location",
        "inventory",
        "location_items",
    }

    if not required_keys.issubset(data):
        raise InvalidLoadError("Save is missing required fields")

    if not isinstance(data["player_name"], str):
        raise InvalidLoadError("Invalid player name")

    if not isinstance(data["current_location"], str):
        raise InvalidLoadError("Invalid location name")

    if not isinstance(data["inventory"], list):
        raise InvalidLoadError("Inventory must be a list")

    if not isinstance(data["location_items"], dict):
        raise InvalidLoadError("Location items must be an object")

    if data["player_name"] != game.player.name:
        raise InvalidNameError("Wrong player name")
    for location_name in data["location_items"]:
        if location_name not in game.locations:
            raise InvalidLoadLocationError(f"Location not  found: {location_name}")

    all_items = {}

    for location in game.locations.values():
        for item in location.items:
            all_items[item.name] = item
    for item_name in data["inventory"]:
        if item_name not in all_items:
            raise InvalidLoadItemError(f"Item not found: {item_name}")
    for item_names in data["location_items"].values():
        for item_name in item_names:
            if item_name not in all_items:
                raise InvalidLoadItemError(f"Item not found: {item_name}")

    if data["current_location"] not in game.locations:
        raise InvalidLoadLocationError(f"Location not  found")
    game.player.current_location = game.locations[data["current_location"]]
    game.player.inventory.clear()

    for location in game.locations.values():
        location.items.clear()
    for item_name in data["inventory"]:
        try:
            game.player.inventory.append(all_items[item_name])
        except KeyError:
            raise InvalidLoadItemError("Item not found")
    for location_name, item_names in data["location_items"].items():
        for item_name in item_names:
            game.locations[location_name].items.append(all_items[item_name])

    print("Game loaded")
    return True