from exceptions import SaveError, LoadError

class Item:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return f"name: {self.name!r}, description: {self.description!r}"

class Exit:
    def __init__(self, destination: str, requires: str | None = None) -> None:
        self.destination = destination
        self.requires = requires
    def __str__(self) -> str:
        return self.destination
    def __repr__(self) -> str:
        return f"destination: {self.destination!r}, requires: {self.requires!r}"

class Location:
    def __init__(self, name: str, description: str, riddle: dict | None = None) -> None:
        self.name = name
        self.description = description
        self.items: list[Item] = []
        self.exits: dict[str, Exit] = {}
        self.riddle = riddle
        self.riddle_solved = False
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return f"name: {self.name!r}, description: {self.description!r}, items: {self.items!r}, exits: {self.exits!r}"
    def add_item(self, item: Item) -> None:
        self.items.append(item)
    def add_exit(self, direction: str, destination: str, requires: str | None = None) -> None:
        self.exits[direction] = Exit(destination, requires)

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
        current_location = self.player.current_location
        if direction not in current_location.exits:
            print("You can't go there")
            return
        exit = current_location.exits[direction]
        if exit.requires is not None:
            has_item = any(item.name == exit.requires for item in self.player.inventory)
            if not has_item:
                print(f"The door is locked. You need: {exit.requires}")
                return
        self.player.current_location = self.locations[exit.destination]

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
            for direction, exit in self.player.current_location.exits.items():
                print(direction, exit.destination)
        else:
            print("No exits")

    def take_item(self, item_name: str) -> None:
        for item in self.player.current_location.items:
            if item.name == item_name:
                self.player.take_item(item)
                return
        print("Item not found")

    def show_inventory(self) -> None:
        if self.player.inventory:
            print("Inventory:")
            for item in self.player.inventory:
                print(item)
        else:
            print("Inventory is empty")

    def solve_riddle(self) -> None:
        location = self.player.current_location
        riddle = location.riddle
        if riddle is None:
            print("No riddle in here")
            return
        if location.riddle_solved:
            print("You already solved the riddle")
            return
        print(riddle["question"])
        answer = input("Your answer: ").strip().lower()
        correct_answer = riddle["answer"].strip().lower()
        if answer != correct_answer:
            print("Wrong. Try again.")
            return
        location.riddle_solved = True
        reward_data = riddle.get("reward")
        if reward_data:
            reward = Item(reward_data["name"], reward_data["description"])
            self.player.inventory.append(reward)
            print(f"You got a {reward.name}")

    def inspect(self, item_name: str) -> None:
        for item in self.player.inventory:
            if item.name == item_name:
                print(item.description)
                return
        print("Item not found")

    def show_help(self) -> None:
        print("Available commands:")
        for direction in self.player.current_location.exits:
            print(f"go {direction}")
        for item in self.player.current_location.items:
            print(f"take {item}")
        print("look")
        print("inventory")
        print("help")
        print("save")
        print("load")

    def process(self, command: str) -> None:
        from saving import save_game, load_save
        command = command.strip()
        if command == "look":
            self.look_around()
        elif command == "inventory":
            self.show_inventory()
        elif command == "help":
            self.show_help()
        elif command.startswith("go "):
            self.move_player(command[3:].strip())
        elif command.startswith("take "):
            self.take_item(command[5:].strip())
        elif command == "riddle":
            self.solve_riddle()
        elif command.startswith("inspect "):
            self.inspect(command[8:].strip())
        elif command == "quit":
            pass
        elif command == "save":
            try:
                save_game(self)
            except SaveError as error:
                print(f"Not able to save: {error}")
        elif command == "load":
            try:
                load_save(self)
            except LoadError as error:
                print(f"Not able to load: {error}")
        elif not command:
            return
        else:
            print("Command not found")

    def run_game(self) -> None:
        while True:
            command = input("> ")
            self.process(command)
            if command == "quit":
                print("Game over")
                break
