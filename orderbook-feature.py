import itertools
import pandas as pd
from feature_engineering.mid_price import cal_mid_price


raw_data = "book-2024-04-26-bithumb-btc.csv"

df = pd.read_csv(raw_data)
group_o = df.groupby(['timestamp'])


for timestamp, gr_o in group_o:
    print(f"Timestamp: {timestamp}")
    gr_bid_level = gr_o[(gr_o.type == 0)]
    gr_ask_level = gr_o[(gr_o.type == 1)]
    mid_price, bid, ask, bid_qty, ask_qty = cal_mid_price (gr_bid_level, gr_ask_level, None)
    print(mid_price, bid, ask, bid_qty, ask_qty)
    break


