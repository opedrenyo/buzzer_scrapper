import psycopg2 as pg2
import csv
import pandas as pd
import datetime
import math

class BB_db():
    def __init__(self, password) -> None:
        self.user = 'postgres'
        self.database = 'bb_scraper'
        self.password = password
        self.conn = pg2.connect(database = self.database, user = self.user, password = self.password)
        self.cur = self.conn.cursor()
        
    def close(self):
        self.conn.close()
        
    def query_insert_weekly_shapes(self, dataframe:pd.DataFrame, nations_dict:dict):
        ## 1: insertamos los valores que no existen en la tabla players
        print("Importing players to bb_scraper database")
        insert_players = """
                    INSERT INTO players (id_player,id_country,name,age) VALUES (%s,%s,%s,%s)
                    ON CONFLICT (id_player) DO UPDATE SET
                    age = EXCLUDED.age;
                    """
        for index, row in dataframe.iterrows():
            self.cur.execute(insert_players,(row.ID,nations_dict[row.Nationality],row.Name,row.Age))
        
        self.conn.commit()
        
        ## 2: insertamos los valores de las countries en la tabla countries. Si no, en los siguientes inserts podemos tener violaciones de PK.
        print("Importing team countries information to bb_scraper database.")
        insert_countries = """
                    INSERT INTO countries (id_country, country) VALUES(%s, %s) 
                    ON CONFLICT ON CONSTRAINT countries_pkey DO NOTHING;
        """
        for key, value in nations_dict.items():
            self.cur.execute(insert_countries, (value, key))
        self.conn.commit()
        #TODO: Deberiamos asegurarnos que la última season ha sido insertada en la bbdd. (Idea1 : mediante un input? "are you sure last season is in db? Idea2: Que la fecha de import este entre start_date y end_date de alguna season en la bbdd?")
        
        ## 3: insertamos los valores en la performance, si hay conflicto, DO NOTHING y sacamos la week a partir de la fecha de inicio de season y la actual.
        print("Importing player's performance to bb_scraper database.")
        insert_performance = """
                    INSERT INTO performance (id_player,id_season,week, dmi, shape) VALUES (%s,%s,%s,%s,%s)
                    ON CONFLICT ON CONSTRAINT performance_pkey DO NOTHING;"""
        for index, row in dataframe.iterrows():  
            start_date_season = self.start_date_season()[0]
        
            start_valid_season = datetime.datetime(int(start_date_season.strftime("%Y")), 
                                               int(start_date_season.strftime("%m")), 
                                               int(start_date_season.strftime("%d")))
            actual_date = pd.to_datetime(row.Date, format='%d/%m/%Y')    
            actual_valid_date = actual_date.to_pydatetime()

            week = math.ceil((actual_valid_date-start_valid_season).days/7)
            self.cur.execute(insert_performance, (row.ID, self.current_season()[0], week, row.DMI, row.Shape))
            
        self.conn.commit()
        
    def insert_new_season(self, season, start_date):
        print(f"Importing season {season} to bb_scraper database")
        end_date = start_date + datetime.timedelta(days=91)
        insert_season = """
                    INSERT INTO seasons (id_season,start_date,end_date) VALUES (%s,%s,%s);
                    """
        self.cur.execute(insert_season, (season, start_date, end_date))
        self.conn.commit()
        
    def current_season(self):
        self.cur.execute("""SELECT id_season FROM seasons ORDER BY id_season DESC LIMIT 1""")
        
        return self.cur.fetchone()
    
    def start_date_season(self):
        self.cur.execute("""SELECT start_date FROM seasons ORDER BY id_season DESC LIMIT 1""")
       
        return self.cur.fetchone()
    
    def current_week(self):
        self.cur.execute("""SELECT week FROM performance ORDER BY week DESC LIMIT 1""")
       
        return self.cur.fetchone()
    
    
    def query_country_export(self, team_nation):
        select_query = f"""SELECT c.country, p.id_player, p.name, perf.week, perf.id_season, perf.dmi, perf.shape
                        FROM performance AS perf INNER JOIN players AS p ON perf.id_player = p.id_player
                        INNER JOIN countries AS c ON p.id_country = c.id_country WHERE c.country = '{team_nation}'
                        ORDER BY name, perf.week """
        
        self.cur.execute(select_query)
        
        return self.cur.fetchall()
        