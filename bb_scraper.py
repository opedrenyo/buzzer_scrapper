from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

class BB_Scraper():
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()
        self.players_nationality = []
        self.players_name = []
        self.players_id = []
        self.players_shape = []
        self.players_dmi = []
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
        self.driver.get("https://www.buzzerbeater.com/")
        self.id_button_click = self.driver.find_element(By.CLASS_NAME, "btn-outline-light").click()
        sleep(2)
        self.user_input = self.driver.find_element(By.ID, "txtLoginUserName").send_keys(self.user_name)
        self.password_input = self.driver.find_element(By.ID, "txtLoginPassword").send_keys(self.password)
        self.submit_userpassword = self.driver.find_element(By.ID, "btnLogin").click()
        sleep(6)

    def get_players_to_csv(self):
        for key,value in self.nationalities_dict.items():
            self.driver.get(f"https://www.buzzerbeater.com/country/{value}/jnt/players.aspx")
            sleep(1)
            self.number_players_html = self.driver.find_element(By.ID, "cphContent_lblNumberOfPlayers")
            self.number_players = int(self.number_players_html.text.split()[0])

            for i in range(4,self.number_players+4):
                player_name_id = self.driver.find_element(By.XPATH, f'/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[1]/div[4]')
                player_shape = self.driver.find_element(By.XPATH, f"/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[2]/div[3]/table/tbody/tr/td[1]/table/tbody/tr[2]/td/a[2]")
                self.players_nationality.append(key)
                self.players_name.append(player_name_id.text.split("(")[0])
                self.players_id.append(player_name_id.text.split("(")[1].replace(")", ""))
                self.players_shape.append(player_shape.text.split("(")[1].replace(")",""))
                player_dmi_id = self.driver.find_element(By.XPATH, f"/html/body/div[2]/form/div[5]/div/div[3]/div[2]/div/div[6]/div[{i}]/div[2]/div[3]/table/tbody/tr/td[1]/table/tbody/tr[2]/td")
                self.players_dmi.append(player_dmi_id.text.split("DMI: ")[1].split("Edad: ")[0].strip())
                
            self.players_allinfo = [self.players_nationality, self.players_name, self.players_id, self.players_shape, self.players_dmi]
            
        self.df = pd.DataFrame(self.players_allinfo).transpose()

        self.df.to_csv("players_analysis.csv", mode = "a", index=False, header=["Nationality", "Name", "ID", "Shape", "DMI"])

        
