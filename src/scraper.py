from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

from utils.utils import clean_string, parse_json_to_attr, save_dict_to_csv


class DriverSettings():
    def __init__(self) -> None:
        self.chrome_driver_exe_path = None
        self.webdriver_options = None
        self.driver_timeout = None
        self.user_data_dir = None
        parse_json_to_attr(self, './settings/webdriver_settings.json')

        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir={self.user_data_dir}")
        options.page_load_strategy = 'normal'
        [options.add_experimental_option(name, vals) 
            for (name, vals) in self.webdriver_options.items()]

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(self.driver_timeout)

    def get_driver(self):
        return self.driver


class XScraper(object):

    BASE_URL = 'https://twitter.com'
    TWITTER_LOGIN_URL =  BASE_URL + '/login'

    def __init__(self) -> None:
        self.driver = DriverSettings().get_driver()
        self._go_to_login_page()

    def scrape_accounts(self, accounts: list, save_to_csv=False):
        """Scrapes tweets from a list of twitter accounts"""
        tweets = dict()
        df = pd.DataFrame(columns=['Account', 'Label', 'Tweet'])

        for account in accounts:
            tweets[account] = self.scrape_tweets(account)

            print(f'*********** ACCOUNT <{account}> ***********')
            pprint(tweets[account])
            for tweet in tweets[account]:
                row = {
                    'Account': account,
                    'Label': 1 if account=='taylorswift13' else 0,
                    'Tweet': tweet
                }
                df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

        if save_to_csv:
            df.to_csv('./tweets.csv')
            # save_dict_to_csv(tweets)

        return tweets
    
    def removeDuplicateHashtag(self, tweet):
        cleanedTweet = ''
        for word in tweet.split():
            if word[0]=='#':
                cleanedTweet += '#' + word[1:].split('#')[0] + ' '
            else:
                cleanedTweet += word + ' '
        return cleanedTweet

    def scrape_tweets(self, handle: str):
        """Scrapes tweets from a given twitter handle"""

        # 1) Navigate to the twitter page
        self.driver.get(self.BASE_URL + '/' + handle)

        # 2) Grab all the tweet web elements
        tweets_html = self.driver.find_elements(
            By.XPATH, '//div[@data-testid="tweetText"]')

        # 3) Extract the text from the tweet web elements
        tweets_text = []
        for tweet_html in tweets_html:
            all_html_children = tweet_html.find_elements(By.XPATH, './/*')
            tweet_strs = [
                clean_string(child.text) for child in all_html_children
            ]
            tweets_text.append(self.removeDuplicateHashtag(''.join(tweet_strs)))

        return tweets_text

    def _go_to_login_page(self):
        self.driver.get(self.TWITTER_LOGIN_URL)
        return self
