from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd
from dbconn import BB_db

class BB_Scraper():
    def __init__(self) -> None:
        self.db_password = input("Database Password: ")
        print("Initializing bb_scraper...")
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Chrome(options= self.options)
        self.players_nationality = []
        self.players_name = []
        self.players_id = []
        self.players_shape = []
        self.players_dmi = []
        self.players_age = []
        self.nationalities_dict = {
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
            "Bosnia": 35
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
        sleep(4)

    def get_players_info(self):
        self.teams_loop = 1
        print("Generating csv... Wait please.")
        for key,value in self.nationalities_dict.items():
            
            self.driver.get(f"https://www.buzzerbeater.com/country/{value}/jnt/players.aspx")
            sleep(0.3)
            self.number_players_html = self.driver.find_element(By.ID, "cphContent_lblNumberOfPlayers")
            self.number_players = int(self.number_players_html.text.split()[0])

            for i in range(4,self.number_players+4):
                player_name_id = self.driver.find_element(By.XPATH, f'/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[1]/div[4]')
                player_shape = self.driver.find_element(By.XPATH, f"/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[2]/div[3]/table/tbody/tr/td[1]/table/tbody/tr[2]/td/a[2]")
                self.players_nationality.append(key)
                self.players_name.append(player_name_id.text.split("(")[0].strip())
                self.players_id.append(player_name_id.text.split("(")[1].replace(")", ""))
                self.players_shape.append(player_shape.text.split("(")[1].replace(")",""))        
                players_info = self.driver.find_element(By.XPATH, f"/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[2]/div[3]/table/tbody/tr/td[1]/table/tbody/tr[2]/td")
                self.players_dmi.append(players_info.text.splitlines()[2].split(": ")[1].strip())
                self.players_age.append(players_info.text.splitlines()[3].split(": ")[1].strip())
             
            self.players_allinfo = [self.players_nationality, self.players_name, self.players_id, self.players_shape, self.players_dmi, self.players_age]
            print(f"Team {key} scraped. {self.teams_loop}/{len(self.nationalities_dict)} to go.")
            self.teams_loop += 1 
            
        self.df = pd.DataFrame(self.players_allinfo).transpose()
        
        self.df.columns = ("Nationality","Name","ID","Shape","DMI","Age")
        
        return self.df



    # JBC - 2023.02.21 - Main menu method
    # inputs: 1 = save week's shape // 2 = export team's shape // 3 = add calendar
    def menu(self):
        
        newLine = '\n'
        option = input("Que desea realizar?" + newLine  + "1 - Guardar formas semanales" + newLine + "2 - Exportar info de una seleccion" + newLine + "3 - Marcar calendario" + newLine)
        print("Opcion elegida: " + option)
        if option.strip() == '1':
            print("Se procede a guardar las formas semanales")
            
            bb_db_conn = BB_db(self.db_password)
            bb_db_conn.insert_weekly_shapes(self.get_players_info())
            bb_db_conn.close()
        elif option.strip() == '2':
            teamId = input("Introduzca el ID del equipo a exportar")
            #TODO implementar metodo de exportacion a traves de la bbdd
            print("Exportando la información del equipo " + teamId)
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
        # format given date to dd/mm/yyyy format
        seasonDate = pd.to_datetime(dateInput, format='%d/%m/%y')
        bb_db_conn = BB_db(self.db_password)
        bb_db_conn.insert_new_season(season, seasonDate)
        bb_db_conn.close()
        # a season has 13 weeks so we will iterate until we have added all weeks of a given season
        for i in range(1, 14):
            print("Insertado T" + season + " semana " + str(i) + " fecha " + seasonDate.strftime('%d/%m/%y'))
            # insert into temporadas(season, i, date)
            seasonDate = seasonDate + pd.DateOffset(days=7)
        
        print("Calendario de la temporada añadido!")





