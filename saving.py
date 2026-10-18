import json


def save_game(game, filename: str = "data/save.json") -> None:
    data = {
        "player_name": game.player.name,
        "current_location": game.player.current_location.name,
        "inventory": [item.name for item in game.player.inventory],
        "location_items": {
            location.name: [item.name for item in location.items] for location in game.locations.values()
        },
    }
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)
    print("Game saved")

def load_save(game, filename: str = "data/save.json") -> bool:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Cannot load save")
        return False

    if data["player_name"] != game.player.name:
        print("Wrong player name")
        return False
    game.player.current_location = game.locations[data["current_location"]]

    all_items = {}

    for location in game.locations.values():
        for item in location.items:
            all_items[item.name] = item

    game.player.inventory.clear()

    for location in game.locations.values():
        location.items.clear()
    for item_name in data["inventory"]:
        game.player.inventory.append(all_items[item_name])
    for location_name, item_names in data["location_items"].items():
        for item_name in item_names:
            game.locations[location_name].items.append(all_items[item_name])

    print("Game loaded")
    return True