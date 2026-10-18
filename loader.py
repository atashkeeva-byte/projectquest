import json
from classes import Location, Item, Player
from exceptions import ScenarioError, MissingStartError, InvalidLocationError, InvalidExitError, InvalidItemError


def load(filename: str) -> dict|None:
    try:
        with open(filename, encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Scenario not found")
        return None
    except json.JSONDecodeError:
        print("Mistake in a scenario")
        return None

def validate(data: dict) -> bool:
    if not isinstance(data, dict):
        raise ScenarioError("Scenario must be a JSON object")
    if "locations" not in data:
        raise InvalidLocationError("Missing locations")
    locations = data["locations"]
    if not isinstance(locations, dict) or not locations:
        raise InvalidLocationError("Locations must be a non-empty dictionary")
    if "start" not in data:
        raise MissingStartError("Missing starting location")
    if not isinstance(data["start"], str):
        raise MissingStartError("Starting location must be a string")
    if data["start"] not in locations:
        raise MissingStartError("Starting location not found")
    for location_name, location_data in locations.items():
        if not isinstance(location_data, dict):
            raise InvalidLocationError(f"Invalid location: {location_name}")
        if "description" not in location_data:
            raise InvalidLocationError(f"Missing description in location {location_name}")
        if not isinstance(location_data["description"], str):
            raise InvalidLocationError(f"Invalid description in location {location_name}")
        if "exits" not in location_data:
            raise InvalidLocationError(f"Missing exits in location {location_name}")
        exits = location_data["exits"]
        if not isinstance(exits, dict):
            raise InvalidLocationError(f"Exits must be a dictionary in {location_name}")
        for direction, destination in exits.items():
            if not isinstance(direction, str) or not direction:
                raise InvalidExitError(f"Invalid exit direction in {location_name}")
            if not isinstance(destination, str):
                raise InvalidExitError(f"Invalid destination in {location_name}")
            if destination not in locations:
                raise InvalidExitError(f"Destination not found: {destination}")
        if "items" not in location_data:
            raise InvalidLocationError(f"Missing items in location {location_name}")
        items = location_data["items"]
        if not isinstance(items, list):
            raise InvalidItemError(f"Items must be a list in {location_name}")
        for item in items:
            if not isinstance(item, dict):
                raise InvalidItemError(f"Invalid item in location {location_name}")
            if "name" not in item or "description" not in item:
                raise InvalidItemError("Item must have a name and description")
            if not isinstance(item["name"], str) or not item["name"]:
                raise InvalidItemError("Item name must be a non-empty string")
            if not isinstance(item["description"], str):
                raise InvalidItemError("Item description must be a string")
    return True

def create_locations(data: dict) -> dict[str, Location]:
    locations = {}
    for location_name, location_data in data["locations"].items():
        locations[location_name] = Location(location_name, location_data["description"])
    for location_name, location_data in data["locations"].items():
        location = locations[location_name]
        for direction, destination in location_data["exits"].items():
            location.add_exit(direction, destination)
        for item_data in location_data["items"]:
            location.add_item(Item(item_data["name"], item_data["description"]))
    return locations

