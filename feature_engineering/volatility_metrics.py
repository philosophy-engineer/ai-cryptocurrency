
def cal_volatility_metrics(mid_price, window_size=10):
    return mid_price.rolling(window=window_size).std().fillna(0)
