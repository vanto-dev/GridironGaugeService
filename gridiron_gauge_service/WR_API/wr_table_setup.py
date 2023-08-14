import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="2022-WR-Database",
    user="postgres",
    password="postgresql_gridirongauge2320",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

create_table_query = """
CREATE TABLE WR_STATS_TABLE_2022 (
    Rank int,
    Name varchar(100),
    Team varchar(10),
    Games int,
    TGTS int,
    REC int,
    PCT varchar(5),
    YDS int,
    TD int,
    LNG int,
    YT varchar(5),
    YR varchar(5),
    RUSH_ATT int,
    RUSH_YDS int,
    RUSH_AVG varchar(5),
    RUSH_TD int,
    RUSH_FUM int,
    RUSH_LST int,
    PPG varchar(5),
    FPTS varchar(10)
);
"""

# Execute the create table query
cur.execute(create_table_query)
# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
