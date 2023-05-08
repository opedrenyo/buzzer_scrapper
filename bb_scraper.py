from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from time import sleep
import pandas as pd
from dbconn import BB_db
from datetime import datetime
import os
from writer import Writer

class BB_Scraper():
    def __init__(self) -> None:
        self.db_password = input("Database Password: ")
        print("Initializing bb_scraper...")
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Chrome(options= self.options)
        self.players_date = []
        self.players_nationality = []
        self.players_name = []
        self.players_id = []
        self.players_shape = []
        self.players_dmi = []
        self.players_age = []
        self.players_jumpshot = []
        self.players_shotrange = []
        self.players_outside_defense = []
        self.players_handling = []
        self.players_driving = []
        self.players_passes = []
        self.players_inside_shot = []
        self.players_inside_defense = []
        self.players_rebounds = []
        self.players_blocks = []
        self.players_resist = []
        self.players_free_throws = []
        self.nationalities_dict = {
            "Spain": 7,
            "Germany": 8, 
            "Belgium": 13,
            "Letonia": 46,
            "Holanda": 16,
            "Irlanda": 44,
            "Austria": 27,
            "Israel": 15,
            "Grecia": 12,
            "Ucrania": 33,
            "Inglaterra": 14,
            "Polonia": 58,
            "Francia": 11,
            "Eslovenia": 66,
            "Romania": 61,
            "Hungria": 48,
            "Italia": 10,
            "Portugal": 18,
            "Finlandia": 69,
            "Lituania": 20,
            "Estonia": 41,
            "Rusia": 19,
            "Serbia": 29,
            "Turquia": 6,
            "Eslovaquia": 67,
            "Bosnia": 35,
            "Ceska":37
        }
        
    def signin(self, username, password):
        self.user_name = username
        self.password = password
        print(f"Signing in {self.user_name} account. Wait please...")
        self.driver.get("https://www.buzzerbeater.com/")
        self.id_button_click = self.driver.find_element(By.CLASS_NAME, "btn-outline-light").click()
        sleep(1)
        self.user_input = self.driver.find_element(By.ID, "txtLoginUserName").send_keys(self.user_name)
        self.password_input = self.driver.find_element(By.ID, "txtLoginPassword").send_keys(self.password)
        self.submit_userpassword = self.driver.find_element(By.ID, "btnLogin").click()
        sleep(3)

    def get_players_info(self):
        self.teams_loop = 1
        for key,value in self.nationalities_dict.items():
            
            self.driver.get(f"https://www.buzzerbeater.com/country/{value}/jnt/players.aspx")
            sleep(0.3)
            self.number_players_html = self.driver.find_element(By.ID, "cphContent_lblNumberOfPlayers")
            self.number_players = int(self.number_players_html.text.split()[0])
            self.select = Select(self.driver.find_element(By.ID, 'cphContent_ddlsortBy'))
            self.select.select_by_value("4")

            for i in range(4,self.number_players+4):
                player_name_id = self.driver.find_element(By.XPATH, f'/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[1]/div[4]')
                player_shape = self.driver.find_element(By.XPATH, f"/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[2]/div[3]/table/tbody/tr/td[1]/table/tbody/tr[2]/td/a[2]")
                self.players_date.append(datetime.now().strftime("%d/%m/%Y"))
                self.players_nationality.append(key)
                self.players_name.append(player_name_id.text.split("(")[0].strip())
                self.players_id.append(player_name_id.text.split("(")[1].replace(")", ""))
                self.players_shape.append(player_shape.text.split("(")[1].replace(")",""))        
                players_info = self.driver.find_element(By.XPATH, f"/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[2]/div[3]/table/tbody/tr/td[1]/table/tbody/tr[2]/td")
                self.players_dmi.append(players_info.text.split("DMI: ")[1].split("Edad: ")[0].strip())
                self.players_age.append(players_info.text.split("Edad: ")[1].split("Altura: ")[0].strip())

                # si hay visibilidad de la tabla de skills es que el jugador esta en venta, lo marcamos para chupar las skills despues
                try:
                    player_skills = self.driver.find_element(By.XPATH, f"/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[2]/div[3]/table/tbody/tr/td[2]/table/tbody")
                except:
                    player_skills = None;

                # puede parecer coñazo pero asi guardamos el valor de todas las skills a traves de la tabla sin importar el idioma
                if player_skills != None:
                    self.players_jumpshot.append(self.driver.find_element(By.XPATH, f"/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[2]/div[3]/table/tbody/tr/td[2]/table/tbody/tr[1]/td[1]/a").text.split("(")[1].replace(")","").strip())
                    self.players_shotrange.append(self.driver.find_element(By.XPATH, f"/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[2]/div[3]/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/a").text.split("(")[1].replace(")","").strip())
                    self.players_outside_defense.append(self.driver.find_element(By.XPATH, f"/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[2]/div[3]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[1]/a").text.split("(")[1].replace(")","").strip())
                    self.players_handling.append(self.driver.find_element(By.XPATH, f"/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[2]/div[3]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/a").text.split("(")[1].replace(")","").strip())
                    self.players_driving.append(self.driver.find_element(By.XPATH, f"/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[2]/div[3]/table/tbody/tr/td[2]/table/tbody/tr[3]/td[1]/a").text.split("(")[1].replace(")","").strip())
                    self.players_passes.append(self.driver.find_element(By.XPATH, f"/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[2]/div[3]/table/tbody/tr/td[2]/table/tbody/tr[3]/td[2]/a").text.split("(")[1].replace(")","").strip())
                    self.players_inside_shot.append(self.driver.find_element(By.XPATH, f"/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[2]/div[3]/table/tbody/tr/td[2]/table/tbody/tr[4]/td[1]/a").text.split("(")[1].replace(")","").strip())
                    self.players_inside_defense.append(self.driver.find_element(By.XPATH, f"/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[2]/div[3]/table/tbody/tr/td[2]/table/tbody/tr[4]/td[2]/a").text.split("(")[1].replace(")","").strip())
                    self.players_rebounds.append(self.driver.find_element(By.XPATH, f"/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[2]/div[3]/table/tbody/tr/td[2]/table/tbody/tr[5]/td[1]/a").text.split("(")[1].replace(")","").strip())
                    self.players_blocks.append(self.driver.find_element(By.XPATH, f"/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[2]/div[3]/table/tbody/tr/td[2]/table/tbody/tr[5]/td[2]/a").text.split("(")[1].replace(")","").strip())
                    self.players_resist.append(self.driver.find_element(By.XPATH, f"/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[2]/div[3]/table/tbody/tr/td[2]/table/tbody/tr[6]/td[1]/a").text.split("(")[1].replace(")","").strip())
                    self.players_free_throws.append(self.driver.find_element(By.XPATH, f"/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[2]/div[3]/table/tbody/tr/td[2]/table/tbody/tr[6]/td[2]/a").text.split("(")[1].replace(")","").strip())
                else:
                    self.players_jumpshot.append(None)
                    self.players_shotrange.append(None)
                    self.players_outside_defense.append(None)
                    self.players_handling.append(None)
                    self.players_driving.append(None)
                    self.players_passes.append(None)
                    self.players_inside_shot.append(None)
                    self.players_inside_defense.append(None)
                    self.players_rebounds.append(None)
                    self.players_blocks.append(None)
                    self.players_resist.append(None)
                    self.players_free_throws.append(None)

            self.players_allinfo = [self.players_date,self.players_nationality, self.players_name, self.players_id,
                                    self.players_shape, self.players_dmi, self.players_age, self.players_jumpshot, self.players_shotrange,
                                    self.players_outside_defense, self.players_handling, self.players_driving, self.players_passes, self.players_inside_shot,
                                    self.players_inside_defense, self.players_rebounds, self.players_blocks, self.players_resist, self.players_free_throws]
            print(f"Team {key} scraped. {self.teams_loop}/{len(self.nationalities_dict)} to go.")
            self.teams_loop += 1 
            
        self.df = pd.DataFrame(self.players_allinfo).transpose()
        
        self.df.columns = ("Date","Nationality","Name","ID","Shape","DMI","Age","Jumpshot","Shot_range","Outside_defense","Handling","Driving","Passes","Inside_shot","Inside_defense","Rebounds","Blocks","Resist","Free_throws")
        
        return self.df



    # JBC - 2023.02.21 - Main menu method
    # inputs: 1 = save week's shape // 2 = export team's shape // 3 = add calendar
    def menu(self):
        
        newLine = '\n'
        option = input("Que desea realizar?" + newLine  + "1 - Guardar formas semanales" + newLine + "2 - Exportar info de una seleccion" + newLine + "3 - Marcar calendario" + newLine)
        print("Opcion elegida: " + option)
        if option.strip() == '1':
            print("Se procede a guardar las formas semanales")
            self.insert_weekly_shapes()
            
        elif option.strip() == '2':
            self.countries = list(self.nationalities_dict.keys())
            self.team_nation = input(f"Introduzca la selección a exportar ({self.countries}):  ").title()
            print("Exportando la información del equipo " + self.team_nation)
            self.export_country_season()
            Writer(self.db_password, self.team_nation)
            
        elif option.strip() == '3':
            season = input("Introduzca el número de temporada" + newLine)
            # esto ya se pulirá para mostrar un calendario y elegir el dia directamente
            dateInput = input("Introduzca la fecha del primer entreno de la temporada en formato DD/MM/YY" + newLine)
            print("Inicializando calendario de la temporada " + season)
            self.initCalendar(season, dateInput)
        else:
            print("Desconectando...")

    # JBC - 2023.02.21 - Given first day of a season, calculate and save the 13 weeks of a season
    # params: season = specifies the season to calculate // dateInput = specifies the first day of season
    def initCalendar(self, season, dateInput):
        # El formato cambia a dd/MM/yyyy hh:mm:ss ya que en BBDD pasa a ser timestamp y haremos calculos segun hora
        # Le añadimos las 13h que es cuando se actualizan las ultimas formas
        dateInput = dateInput + " 13:00:00"
        seasonDate = pd.to_datetime(dateInput, format='%d/%m/%Y %H:%M:%S')
        bb_db_conn = BB_db(self.db_password)
        bb_db_conn.insert_new_season(season, seasonDate)
        bb_db_conn.close()
        # a season has 13 weeks so we will iterate until we have added all weeks of a given season
        for i in range(1, 14):
            print("Insertado T" + season + " semana " + str(i) + " fecha " + seasonDate.strftime('%d/%m/%Y'))
            # insert into temporadas(season, i, date)
            seasonDate = seasonDate + pd.DateOffset(days=7)
        
        print("Calendario de la temporada añadido!")
        
    def export_country_season(self):
        bb_db_conn = BB_db(self.db_password)
        export_data = bb_db_conn.query_country_export(self.team_nation)
        df_export = pd.DataFrame(export_data, columns=["Nationality", "ID_player", "Name", "Week", "Season", "DMI", "Shape"])
        dir_exists = os.path.exists(f"exports/{self.team_nation}")
        if not dir_exists:
            os.makedirs(f"exports/{self.team_nation}")
        
        df_export.to_csv(f"exports/{self.team_nation}/{self.team_nation}_W{bb_db_conn.current_week()[0]}_T{bb_db_conn.current_season()[0]}.csv", index=False)    
        
        bb_db_conn.close()
        
    def insert_weekly_shapes(self):
        bb_db_conn = BB_db(self.db_password)
        bb_db_conn.query_insert_weekly_shapes(self.get_players_info(), self.nationalities_dict)
        bb_db_conn.close()
        

        
        
        
        





