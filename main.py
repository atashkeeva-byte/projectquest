print("Welcome")
from loader import load, validate, create_locations
from classes import Game
from exceptions import ScenarioError

def main() -> None:
    data = load("data/quest.json")
    if data is None:
        print("Not able to continue")
        return
    try:
        validate(data)
        locations = create_locations(data)
    except ScenarioError as error:
        print(f"Scenario Error: {error}")
        return
    name = input("Enter player name: ")
    game = Game(locations, data["start"], name)
    game.run_game()

if __name__ == "__main__":
    main()