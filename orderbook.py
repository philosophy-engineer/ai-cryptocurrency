import datetime
from bithumb import Bithumb


class AiCryptoClient:

    bithumb = Bithumb()
    coins = ["BTC_KRW", "ETH_KRW", "SOL_KRW"]


    def get_day_orderbook(self):
        now = datetime.datetime.now()
        tomorrow = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        i = 0
        while(datetime.datetime.now() < tomorrow):
            i += 1
            if i == 1e7:
                print(f"Waiting {tomorrow} to get order book from start of the day.")
                i = 0
        self.bithumb.get_orderbook(self.coins, 5)



if __name__ == "__main__":
    client = AiCryptoClient()
    client.get_day_orderbook()



