import requests
from Config import keys

class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quota: str, base: str, amount: float):
        if quota == base:
            raise ConvertionException(f'Невозможно перевести одинаковую валюту {base}.')
        try:
            quote_ticker = keys[quota]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quota}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        response = requests.get(
            f"https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}",
            params={"api_key": "3a252c22c33028dfe2a0c6e11427322d009058abe3100cd6aad6800dcf36e47f"},
            headers={"Content-type": "application/json; charset=UTF-8"}
        )



        data = response.json()
        if quote_ticker not in data:
            raise ConvertionException(f'Не удалось получить курс для валюты {quota}')

        conversion_rate = data[quote_ticker]
        total_base = round((amount /conversion_rate),2)
        return total_base