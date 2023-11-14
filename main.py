from src.scraper import XScraper

accounts = [
    'OnlyInBOS',
    'taylorswift13',
    'Avengers',
]

if __name__ == "__main__":
    bot = XScraper()

    tweets = bot.scrape_accounts(accounts=accounts)
