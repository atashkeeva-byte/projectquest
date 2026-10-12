class Item:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return f"name: {self.name!r}, description: {self.description!r}"

class Location:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description
        self.items: list[Item] = []
        self.exits: dict[str, str] = {}
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return f"name: {self.name!r}, description: {self.description!r}, items: {self.items!r}, exits: {self.exits!r}"
    def add_item(self, item: Item) -> None:
        self.items.append(item)
    def add_exit(self, direction: str, location_name: str) -> None:
        self.exits[direction] = location_name

class Player:
    def __init__(self, name: str, location: Location) -> None:
        self.name = name
        self.current_location = location
        self.inventory: list[Item] = []
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return f"name: {self.name!r}, location: {self.current_location!r}, inventory: {self.inventory!r}"
    def take_item(self, item: Item) -> None:
        self.inventory.append(item)
        self.current_location.items.remove(item)

class Game:
    def __init__(self, locations: dict[str, Location], start_location: str) -> None:
        self.locations = locations
        self.start_location = start_location

