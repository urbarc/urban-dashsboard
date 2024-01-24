import json
from os import system
import psycopg2 as postgres
from color import bold_bright_red, bold_bright_green, default

# "sessions/database-env.json"
class UrbanDB:
    def __init__(self, env_file):
        try:
            env = json.load(open(env_file, 'r'))
            self.connection = postgres.connect(env["DB_URL"])
            self.cursor = self.connection.cursor()

            # printing debug messages simiillar to kivy
            print(f"[{bold_bright_green}INFO{default}   ] [Postgres    ] Database connected successfully.")
        except json.JSONDecodeError:
            print(f"[{bold_bright_red}ERROR{default}  ] [JSON         ] Error Decoding the database JSON file.")
        except Exception as e:
            print(f"[{bold_bright_red}ERROR{default}  ] [Postgres     ] Database not connected successfully.")
            print(f"[{bold_bright_red}ERROR{default}  ] [             ] {e}.")

    def close(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def create(self, table_name, **kwargs):
        try:
            columns = ", ".join([f"{key} {value}" for key, value in kwargs.items()])
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});")
        except Exception as e:
            print(f"[{bold_bright_red}ERROR{default}  ] [Postgres     ] Could not create table ({table_name}) in database.")
            print(f"[{bold_bright_red}ERROR{default}  ] [             ] {e}.")
    
    def drop(self, table_name):
        try:
            self.cursor.execute(f"DROP TABLE {table_name}")
        except Exception as e:
            print(f"[{bold_bright_red}ERROR{default}  ] [Postgres     ] Could not drop table ({table_name}) in database.")
            print(f"[{bold_bright_red}ERROR{default}  ] [             ] {e}.")
