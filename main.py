from bb_scraper import BB_Scraper

username = input("Username: ")
password = input("Password: ")

username = 'badino14'
password = 'ilovebasket14'
bb_scraper = BB_Scraper()

bb_scraper.signin(username, password)

bb_scraper.menu()

bb_scraper.driver.quit()
