from bb_scraper import BB_Scraper

# username = input("Username: ")
# password = input("Password: ")

bb_scraper = BB_Scraper()

bb_scraper.signin('badino14', 'ilovebasket14')

bb_scraper.menu()

bb_scraper.driver.quit()
