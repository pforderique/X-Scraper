from src.scraper import XScraper

accounts = [
    'OnlyInBOS',
    'taylorswift13',
    'Avengers',
    'NVIDIAAIDev'
]

if __name__ == "__main__":
    bot = XScraper()

    tweets = bot.scrape_accounts(accounts=accounts, save_to_csv=True)
