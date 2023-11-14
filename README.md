# X Scraper

Scrapes tweets from twitter.com. Used for educational purposes only (NLP final project).

## How to use
1) Download the code
2) Download a [chromedriver](https://chromedriver.chromium.org/downloads) and update the path in `settings/webdriver_settings.json` to point to it
2) Open `main.py` and edit the accounts you want to scrape from
3) Run `main.py`

## Known Issues
* Sometimes modals popup and get in the way... forces you to restart the scraper :(
* Some tweets end in "..." because the bot currently does not click the "See More" button to expand tweets list
* Saving to CSV is not supported yet
* Some tweets are broken up, so we need to find a way to stitch them back