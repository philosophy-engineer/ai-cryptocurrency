import time
import datetime
import pandas as pd
import requests


class Bithumb:
    def get_orderbook(self, coins: list, count: int) -> None:
        time_interval = 4.9
        orderbooks = {}
        now = datetime.datetime.now()
        end_time = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

        while True:
            for coin in coins:
                request_time = datetime.datetime.now()
                response = requests.get(f"https://api.bithumb.com/public/orderbook/{coin}/?count={count}")
                book = response.json()
                data = book['data']

                bids = (pd.DataFrame(data['bids'])).apply(pd.to_numeric)
                bids.sort_values('price', ascending=False, inplace=True)
                bids = bids.reset_index(); del bids['index']
                bids['type'] = 0

                asks = (pd.DataFrame(data['asks'])).apply(pd.to_numeric)
                asks.sort_values('price', ascending=True, inplace=True)
                asks['type'] = 1 

                df = pd.concat([bids, asks])
                df["timestamp"] = request_time

                if coin in orderbooks:
                    orderbooks[coin] = pd.concat([orderbooks[coin], df])
                else:
                    orderbooks[coin] = df
                print(df)
            print("========================")
            if datetime.datetime.now() + datetime.timedelta(seconds=time_interval) > end_time:
                day = datetime.datetime.strftime(end_time + datetime.timedelta(-1), "%Y-%m-%d")
                for coin in coins:
                    orderbooks[coin].to_csv(f"crypto_data/{coin}/book-{day}-bithumb-{coin[:3].lower()}.csv", index=False)
                    del orderbooks[coin]
                end_time += datetime.timedelta(1)
                print("\n\n######################")
                print(end_time)
                print("######################\n\n")
            else:
                time.sleep(time_interval)

if __name__ == "__main__":
    coins = ["BTC_KRW", "ETH_KRW", "SOL_KRW"]

    bithumb = Bithumb()
    bithumb.get_orderbook(coins, 5)

