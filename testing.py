from classes import Item, Location, Player
print("start")
item = Item("pen", "ink pen")
loc = Location("classroom", "windows are open")
player = Player("Finn", loc)
loc.items.append(item)
player.take_item(item)
print(repr(player))
print(repr(loc))

print("end")