from dbconn import BB_db
import pandas as pd
import os

class Writer():
    def __init__(self, db_password, country, type_writing = "forumpost_weekly_shape_analysis") -> None:
        self.country = country
        self.type = type_writing
        self.db_password = db_password
        bb_db_conn = BB_db(self.db_password)
        self.current_season = bb_db_conn.current_season()[0]
        self.current_week = bb_db_conn.current_week()[0]
        bb_db_conn.close()
        if self.type == "forumpost_weekly_shape_analysis":
            self.weekly_shape_article()
    
    
    def bold(self, string):
        return f"[b]{string}[/b]"
    
    def underline(self,string):
        return f"[u]{string}[/u]"
    
    def bold_underline(self,string):
        return f"[b][u]{string}[/u][/b]"
    
    def weekly_shape_article(self):
        #TODO: Ampliar con posiciones y entrenos.
        df = pd.read_csv(f"exports/{self.country}/{self.country}_W{self.current_week}_T{self.current_season}.csv")
        df_unique_players_id = df[["ID_player", "Name"]].drop_duplicates(["ID_player"])
        
        formatted_player_ID_list = []
        title = self.bold_underline("JUGADORES")
        
        for index,row in df_unique_players_id.iterrows(): 
            formatted_player_ID_list.append(self.bold_underline(f"{row.Name} [player={row.ID_player}]"))  
        dir_exists = os.path.exists(f"forumpost/{self.country}")
        if not dir_exists:
            os.makedirs(f"forumpost/{self.country}")
        with open(f"forumpost/{self.country}/T{self.current_season}_W{self.current_week}-{self.country}_forumpost_weekly_shape_analysis.txt", "w", encoding="UTF-8") as file:
                file.write(f"{title}\n\n")
                for player in formatted_player_ID_list:
                    player_name = player.split("[u]")[1].split("[")[0].strip()
                    df_shape_dmi = df[["Shape", "DMI"]].loc[df.Name == player_name]
                    for index,row in df_shape_dmi.iterrows():
                        file.write(f"{player} -->")
                        if not index == df_shape_dmi.index[-1]:
                            file.write(f" F{row.Shape}: {row.DMI} //")
                        else:
                            file.write(f" F{row.Shape}: {self.bold(row.DMI)}\n\n")