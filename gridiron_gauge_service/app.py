from flask import Flask
import psycopg2
from flask_cors import CORS

from gridiron_gauge_service.search_sleeper_json import get_wrs

app = Flask(__name__)
CORS(app)


@app.route("/api/wide_receiver_data")
def get_wide_receiver_data():
    wr_dict = get_wrs()
    wr_info_response = []

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
    select_query = "SELECT rank, name, TGTS FROM wr_stats_table_2022"

    # Execute the query
    cur.execute(select_query)

    # Fetch all rows (player names)
    player_data = cur.fetchall()

    # Print the player names
    for rank, name, tgts in player_data:
        if not tgts or tgts < 15:
            continue
        player_entry = {}
        if name:

            player_entry["name"] = name
            player_entry["score"] = tgts

            espn_id = search_sleeper_response_for_wr(name, wr_dict)
            if espn_id == "no id found":
                player_entry["playerPhoto"] = ("https://www.pro-"
                                               "football-reference.com/req/20230307/images/headshots/StxxAm00_2022.jpg")
            else:
                player_entry["playerPhoto"] = ("https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/" +
                                               str(espn_id) + ".png&w=350&h=254")

            wr_info_response.append(player_entry)

    # Close the cursor and connection
    cur.close()
    conn.close()
    return wr_info_response


def search_sleeper_response_for_wr(player_name, wr_dict):
    for player in wr_dict.values():
        full_name = player["full_name"]
        if full_name in player_name:
            if player["espn_id"]:
                return player["espn_id"]
            else:
                return "no id found"
