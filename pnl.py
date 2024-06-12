import pandas as pd


def calculate_pnl(filename, init_capital):
    btc_data = pd.read_csv(filename)

    btc_data['hold'] = btc_data.apply(lambda row: row['quantity'] if row['side'] == 0 else -row['quantity'], axis=1)
    btc_data['hold'] = btc_data['hold'].cumsum()

    money_values = []
    coin_values = []
    total_values = []
    pnls = []
    for i, row in btc_data.iterrows():
        if i != 0:
            money_value = row['amount'] + money_values[i-1]
            coin_value = row['hold'] * row['price']
            total_value = money_value + coin_value
            pnl = total_value - total_values[i-1]

        else:
            money_value = row['amount'] + init_capital
            coin_value = row['hold'] * row['price']
            total_value = money_value + coin_value
            pnl = total_value - init_capital

        money_values.append(money_value)
        coin_values.append(coin_value)
        total_values.append(total_value)
        pnls.append(pnl)
        
    btc_data['money'] = money_values
    btc_data['coin'] = coin_values
    btc_data['total'] = total_values
    btc_data['PnL'] = pnls
    btc_data['Cumulative_PnL'] = btc_data['PnL'].cumsum()
            
    pd.options.display.float_format = '{:,.6f}'.format
    print(btc_data)
    print()

    max_pnl = btc_data[btc_data['PnL'] == max(btc_data['PnL'])]['PnL'].iloc[0]
    min_pnl = btc_data[btc_data['PnL'] == min(btc_data['PnL'])]['PnL'].iloc[0]
    max_cumulative_pnl = btc_data[btc_data['Cumulative_PnL'] == max(btc_data['Cumulative_PnL'])]['Cumulative_PnL'].iloc[0]
    min_cumulative_pnl = btc_data[btc_data['Cumulative_PnL'] == min(btc_data['Cumulative_PnL'])]['Cumulative_PnL'].iloc[0]

    print("Max PnL:", max_pnl)
    print("Min PnL:", min_pnl)
    print("Max cumlative PnL", max_cumulative_pnl)
    print("Min cumlative PnL", min_cumulative_pnl)
    print()

    output_file_path = f'{filename[:-4]}-with-pnl.csv'
    btc_data.to_csv(output_file_path, index=False)


if __name__ == "__main__":
    calculate_pnl("ai-crypto-project-3-live-btc-krw.csv", 1e8)
