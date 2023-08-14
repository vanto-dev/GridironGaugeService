import psycopg2
import json

database_path = "WR_API/sleeper_api_response.json"

conn = psycopg2.connect(
    dbname="2022-WR-Database",
    user="postgres",
    password="postgresql_gridirongauge2320",
    host="localhost",
    port="5432"
)

# Create a cursor
cur = conn.cursor()

# SQL query to retrieve player names
select_query = "SELECT * FROM wr_stats_table_2022"

# Execute the query
cur.execute(select_query)

# Fetch the column names (headers)
column_names = [desc[0] for desc in cur.description]

# Fetch all rows
player_data = cur.fetchall()

# Store converted entries in a list of dictionaries
player_entries = []

for row in player_data:
    entry_dict = dict(zip(column_names, row))
    player_entries.append(entry_dict)

player_scores = {}
player_ages = {}


def create_age_list():
    with open(database_path, 'r') as file:
        database = json.load(file)
    wr_age_list = []
    for key, value in database.items():
        if value["position"] in ["WR"]:
            wr_age_entry = {"name": value["full_name"], "age": value["age"]}
            if "situation_change" in value.keys():
                wr_age_entry["situation_change"] = value["situation_change"]
            wr_age_list.append(wr_age_entry)
    return wr_age_list


wr_age_list = create_age_list()


def get_score(player_name):
    if not player_name:
        return 0.0
    for player in player_entries:
        if not player["name"]:
            return 0.0
        if player["name"] in player_name:
            if not player["ppg"]:
                continue
            name = str(player["name"])
            situation_change = None
            age = None
            for i in wr_age_list:
                if i["name"] in name:
                    age = int(i["age"])
                    if "situation_change" in i.keys():
                        situation_change = i["situation_change"]
                    break
            if not age:
                continue

            score = 0.0
            if 23 <= age <= 30:
                score += 75
            elif age >= 30:
                diff = age - 29
                score -= (25*diff)
            elif age < 23:
                score -= 0

            score += float(player["ppg"]) * .3
            score += float(player["fpts"]) * .15
            if float(player["fpts"]) < 100 and float(player["games"]) >= 8:
                score -= 100
            score += float(player["tgts"]) * .1
            score += float(player["rec"]) * .1
            score += float(player["pct"]) * .05
            score += float(player["yds"]) * .15
            score += float(player["td"]) * .3
            score += float(player["lng"]) * .025
            score += float(player["yt"]) * .05
            score += float(player["yr"]) * .05
            score += float(player["rush_yds"]) * .02
            score += float(player["rush_avg"]) * .02
            score += float(player["rush_td"]) * .02
            score -= float(player["rush_fum"]) * .02

            if 11 >= player["games"] >= 4:
                score += ((17 - player["games"]) * 15)

            if situation_change:
                score += 15*situation_change

            score /= 50

            truncated_score = round(score, 2)
            return truncated_score
