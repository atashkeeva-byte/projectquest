from loader import load, validate, create_locations

data = load("data/quest.json")

if data is not None:
    validate(data)
    print("Validation finished")
    locations = create_locations(data)
    print(locations)
    print(locations["Комната"].name)
    print(locations["Комната"].description)
    print(locations["Комната"].items)
    print(locations["Комната"].exits)
