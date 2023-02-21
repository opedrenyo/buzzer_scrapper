from bb_scraper import BB_Scraper

username = input("Username: ")
password = input("Password: ")

bb_scraper = BB_Scraper()

bb_scraper.signin(username, password)

bb_scraper.menu()

bb_scraper.driver.quit()
