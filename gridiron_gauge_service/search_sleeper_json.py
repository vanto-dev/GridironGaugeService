import json


def get_wrs():
    database_path = "./sleeper_api_response.json"

    with open(database_path, 'r') as file:
        database = json.load(file)

    player_dict = {}

    for key, value in database.items():
        if value["position"] in ["WR"]:
            player_dict[key] = value

    return player_dict
