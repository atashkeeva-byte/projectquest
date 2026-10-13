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
    def __init__(self, locations: dict[str, Location], start_location: str, player_name: str) -> None:
        self.locations = locations
        self.start_location = start_location
        if start_location not in locations:
            raise ValueError("Start location not found")
        location = locations[start_location]
        self.player = Player(player_name, location)
    def move_player(self, direction: str) -> None:
        if direction not in self.player.current_location.exits:
            print("You can't go there")
            return
        destination_name = self.player.current_location.exits[direction]
        self.player.current_location = self.locations[destination_name]
    def look_around(self) -> None:
        print(self.player.current_location.name)
        print(self.player.current_location.description)
        if self.player.current_location.items:
            print("Items:")
            for item in self.player.current_location.items:
                print(item)
        else:
            print("No items")
        if self.player.current_location.exits:
            print("Exits:")
            for direction, location_name in self.player.current_location.exits.items():
                print(direction, location_name)
        else:
            print("No exits")
    def take_item(self, item_name: str) -> None:
        for item in self.player.current_location.items:
            if item.name == item_name:
                self.player.take_item(item)
                return
        print("Item not found")


