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
                    df_player_info = df[["Shape", "DMI", "Jumpshot", "Shotrange", "OutsideDefense", "Handling", "Driving",
                                        "Passes", "InsideShot", "InsideDefense", "Rebounds", "Blocks", "Resist", "FreeThrows"]].loc[df.Name == player_name]
                    file.write(f"{player} -->")
                    for index,row in df_player_info.iterrows():
                        if not index == df_player_info.index[-1]:
                            file.write(f" F{int(row.Shape)}: {int(row.DMI)} //")
                        else:
                            file.write(f" F{int(row.Shape)}: {self.bold(int(row.DMI))}\n\n")
                            if row.Jumpshot is not None and not pd.isna(row.Jumpshot):
                                file.write(f" Tiro: {int(row.Jumpshot)}\t\t Alcance: {int(row.Shotrange)}\n\n")
                                file.write(f" DE: {int(row.OutsideDefense)}\t\t Manejo: {int(row.Handling)}\n\n")
                                file.write(f" Pen: {int(row.Driving)}\t\t Pases: {int(row.Passes)}\n\n")
                                file.write(f" TI: {int(row.InsideShot)}\t\t DI: {int(row.InsideDefense)}\n\n")
                                file.write(f" Reb: {int(row.Rebounds)}\t\t Tapones: {int(row.Blocks)}\n\n")
                                file.write(f" Resis: {int(row.Resist)}\t\t TL: {int(row.FreeThrows)}\n\n")