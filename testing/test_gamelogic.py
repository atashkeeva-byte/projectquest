from classes import Game, Location, Item


def make_game():
    room = Location("Комната", "Маленькая комната")
    corridor = Location("Коридор", "Длинный коридор")
    key = Item("Ключ", "Старый железный ключ")
    room.add_item(key)
    room.add_exit("север", "Коридор", "Ключ")
    corridor.add_exit("юг", "Комната")
    locations = {
        "Комната": room,
        "Коридор": corridor,
    }
    return Game(locations, "Комната", "Игрок")


def test_move_with_key():
    game = make_game()
    game.take_item("Ключ")
    game.move_player("север")
    assert game.player.current_location.name == "Коридор"


def test_move_without_key():
    game = make_game()
    game.move_player("север")
    assert game.player.current_location.name == "Комната"


def test_take_item():
    game = make_game()
    game.take_item("Ключ")
    assert len(game.player.inventory) == 1
    assert game.player.inventory[0].name == "Ключ"
    assert len(game.player.current_location.items) == 0