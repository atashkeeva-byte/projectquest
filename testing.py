from classes import Item, Location, Player, Game

# Подготавливаем игру
room = Location("Комната", "Небольшая тёмная комната.")
corridor = Location("Коридор", "Длинный коридор.")

key = Item("Ключ", "Старый железный ключ")
room.add_item(key)
room.add_exit("север", "Коридор")
corridor.add_exit("юг", "Комната")

locations = {
    "Комната": room,
    "Коридор": corridor,
}

game = Game(locations, "Комната", "Игрок")


# Тест 1: осмотр комнаты
print("=== Тест 1: look ===")
game.process("look")


# Тест 2: переход на север
print("\n=== Тест 2: go север ===")
game.process("go север")
print("Текущая локация:", game.player.current_location.name)


# Тест 3: подбор ключа
print("\n=== Тест 3: take Ключ ===")
game.process("go юг")  # Возвращаемся в комнату
game.process("take Ключ")
print("Инвентарь:", game.player.inventory)
print("Предметы в комнате:", room.items)


# Тест 4: неизвестная команда
print("\n=== Тест 4: неизвестная команда ===")
game.process("dance")
game.run_game()