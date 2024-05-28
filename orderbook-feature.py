import pandas as pd
import glob
from feature_engineering.mid_price import cal_mid_price
from feature_engineering.book_imbalance import live_cal_book_i_v1
from feature_engineering.volatility_metrics import cal_volatility_metrics


MID_PRICE_TYPES = ["plain", 'wt', "mkt"]
COINS = ["BTC_KRW", "ETH_KRW"]

def get_features(coins: list, mid_price_types: list):
    for coin in coins:
        file_path = f"./crypto_data/{coin}/*.csv"
        csv_files = glob.glob(file_path)

        data_frames = [pd.read_csv(file) for file in csv_files]
        raw_data = pd.concat(data_frames, ignore_index=True)

        group_o = raw_data.groupby(['timestamp'])

        is_first_line = True
        features = []
        for timestamp, gr_o in group_o:
            row = []
            cols = []
            row.append(timestamp[0])
            cols.append("timestamp")

            gr_bid_level = gr_o[(gr_o.type == 0)]
            gr_ask_level = gr_o[(gr_o.type == 1)]

            for mid_price_type in MID_PRICE_TYPES:
                mid_price, _, _, _, _ = cal_mid_price(gr_bid_level, gr_ask_level, None, mid_price_type)

                if mid_price == -1:
                    continue
                row.append(mid_price)
                cols.append(f"mid_price_{mid_price_type}")

                for param in [(0.2, 5, 1), (0.5, 5, 1)]:
                    bi = live_cal_book_i_v1(
                        param=param,
                        gr_bid_level=gr_bid_level,
                        gr_ask_level=gr_ask_level,
                        diff=None,
                        var={'_flag': is_first_line},
                        mid=mid_price
                    )
                    row.append(bi)
                    cols.append(f"book-imbalance-{mid_price_type}-{param[0]}-{param[1]}-{param[2]}")

            features.append(row)
            if is_first_line:
                is_first_line = False


        features_df = pd.DataFrame(features, columns=cols)
        for mid_price_type in MID_PRICE_TYPES:
            features_df[f"mid_price_{mid_price_type}_volatility"] = cal_volatility_metrics(features_df[f"mid_price_{mid_price_type}"])

        pd.set_option('display.max_columns', None)
        print(features_df.head(20))

        features_df.to_csv(
            f"./crypto_feature/{coin}/features-2024-04-26-2024-04-27-bithumb-{coin[:3].lower()}.csv", 
            index=False
        )


if __name__ == "__main__":
    get_features(COINS, MID_PRICE_TYPES)

