import json
from classes import Location, Item, Player
from exceptions import ScenarioError, MissingStartError, InvalidLocationError, InvalidExitError, InvalidItemError, InvalidRiddleError


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

    item_names = set()

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

        for direction, exit_data in exits.items():
            if not isinstance(direction, str) or not direction:
                raise InvalidExitError(f"Invalid exit direction in {location_name}")
            if isinstance(exit_data, str):
                destination = exit_data
            elif isinstance(exit_data, dict):
                if "destination" not in exit_data:
                    raise InvalidExitError(f"Missing destination in {location_name}")
                destination = exit_data["destination"]
                if not isinstance(destination, str):
                    raise InvalidExitError(f"Invalid destination in {location_name}")
                requires = exit_data.get("requires")
                if requires is not None and (not isinstance(requires, str) or not requires):
                    raise InvalidExitError(f"Invalid condition in {location_name}")
            else:
                raise InvalidExitError(f"Invalid destination in {location_name}")
            if destination not in locations:
                raise InvalidExitError(f"Destination not found: {destination}")

        if "items" not in location_data:
            raise InvalidItemError(f"Missing items in location {location_name}")

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
            item_names.add(item["name"])
            if not isinstance(item["description"], str):
                raise InvalidItemError("Item description must be a string")

        riddle = location_data.get("riddle")

        if riddle is not None:
            if not isinstance(riddle, dict):
                raise InvalidRiddleError(f"Invalid riddle in {location_name}")
            if riddle.get("type") != "question":
                raise InvalidRiddleError(f"Invalid riddle type in {location_name}")
            if not isinstance(riddle.get("question"), str) or not riddle["question"].strip():
                raise InvalidRiddleError(f"Missing riddle question in {location_name}")
            if not isinstance(riddle.get("answer"), str) or not riddle["answer"].strip():
                raise InvalidRiddleError(f"Missing riddle answer in {location_name}")
            reward = riddle.get("reward")

            if reward is not None:
                if not isinstance(reward, dict):
                    raise InvalidRiddleError(f"Invalid reward in {location_name}")
                if not isinstance(reward.get("name"), str) or not reward["name"].strip():
                    raise InvalidRiddleError(f"Invalid reward name in {location_name}")
                if not isinstance(reward.get("description"), str):
                    raise InvalidRiddleError(f"Invalid reward description in {location_name}")

    for location_name, location_data in locations.items():
        for direction, exit_data in location_data["exits"].items():
            if isinstance(exit_data, dict):
                requires = exit_data.get("requires")
                if requires is not None and requires not in item_names:
                    raise InvalidExitError(f"Required item not found: {requires}")
    return True

def create_locations(data: dict) -> dict[str, Location]:
    locations = {}
    for location_name, location_data in data["locations"].items():
        locations[location_name] = Location(location_name, location_data["description"], location_data.get("riddle"))
    for location_name, location_data in data["locations"].items():
        location = locations[location_name]
        for direction, exit_data in location_data["exits"].items():
            if isinstance(exit_data, str):
                location.add_exit(direction, exit_data)
            else:
                destination = exit_data["destination"]
                requires = exit_data.get("requires")
                location.add_exit(direction, destination, requires)
        for item_data in location_data["items"]:
            location.add_item(Item(item_data["name"], item_data["description"]))
    return locations

