import psycopg2 as pg2
import csv
import pandas as pd
import datetime

class BB_db():
    def __init__(self, password) -> None:
        self.user = 'postgres'
        self.database = 'bb_scraper'
        self.password = password
        self.conn = pg2.connect(database = self.database, user = self.user, password = self.password)
        self.cur = self.conn.cursor()
        
    def close(self):
        self.conn.close()
        
    def insert_weekly_shapes(self, dataframe: pd.DataFrame):
        ## Primero insertamos los valores que no existen en la tabla players
        print("Importing players to bb_scraper database")
        insert_players = """
                    INSERT INTO players (id_player,name,age) VALUES (%s,%s,%s)
                    ON CONFLICT (id_player) DO UPDATE SET
                    age = EXCLUDED.age;
                    """
        for index, row in dataframe.iterrows():
            self.cur.execute(insert_players,(row.ID,row.Name,row.Age))
        
        self.conn.commit()
        print("Importing ")
        
    def insert_new_season(self, season, start_date):
        print(f"Importing season {season} to bb_scraper database")
        end_date = start_date + datetime.timedelta(days=91)
        insert_season = """
                    INSERT INTO seasons (id_season,start_date,end_date) VALUES (%s,%s,%s);
                    """
        self.cur.execute(insert_season, (season, start_date, end_date))
        self.conn.commit()
        
        
        