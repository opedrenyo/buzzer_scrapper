from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
from bb_scraper import BB_Scraper

username = "badino14"
password = "ilovebasket14"

bb_scraper = BB_Scraper()

bb_scraper.signin(username, password)

bb_scraper.get_players_to_csv()

bb_scraper.driver.quit()
