from classes import Item, Location, Player, Game
key = Item("Ключ", "Старый железный ключ")
room = Location("Комната", "Тёмная комната.")
room.add_item(key)

game = Game({"Комната": room}, "Комната", "Игрок")

game.take_item("Ключ")
print(game.player.inventory)
print(room.items)