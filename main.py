import tweepy
import requests
import json

class CurrencyRatesFetcher:
    currency_codes: tuple

    def __init__(self, searched_currency_codes: tuple):
        self.url = 'http://api.nbp.pl/api/exchangerates/tables/A'
        self.currency_codes = searched_currency_codes

    def get_currency_rates(self) -> tuple[str, list]:
        response = requests.get(url=self.url)
        data = response.json()
        effective_date = data[0]['effectiveDate']
        searched_rates = [rate for rate in data[0]['rates'] if rate['code'] in self.currency_codes]
        return effective_date, searched_rates


if __name__ == '__main__':
    with open('keys.json', 'r') as f:
        data = json.load(f)
        keys = data['keys']

    searched_currency_codes = ('EUR', 'USD')
    effective_date, currency_rates = CurrencyRatesFetcher(searched_currency_codes).get_currency_rates()

    text = f"Dnia [{effective_date}] kurs złotego wynosi:\n"
    for rate in currency_rates:
        currency = rate['currency']
        mid = round(rate['mid'], 2)
        text += f"\n{currency}: {mid} zł"

    client = tweepy.Client(
        bearer_token=keys['BEARER_TOKEN'],
        consumer_key=keys['API_KEY'],
        consumer_secret=keys['API_KEY_SECRET'],
        access_token=keys['ACCESS_TOKEN'],
        access_token_secret=keys['ACCESS_TOKEN_SECRET'],
    )
    client.create_tweet(text=text)
