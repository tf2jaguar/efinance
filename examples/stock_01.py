import efinance as ef


def strategy_01(_row):
    for i in range(len(df)):
        if i == 0:
            continue
        cur_time = df.iloc[i, 2]
        cur_turnover = df.iloc[i, 7]
        cur_turnover_rate = df.iloc[i, 12]
        last_turnover = df.iloc[i - 1, 7]
        if cur_turnover > last_turnover * 1.66:
            print('交易量相较于前一天放大 时间: %s  昨天: %s 今天: %s 今天换手率: %s' %
                  (cur_time, last_turnover, cur_turnover, cur_turnover_rate))


if __name__ == '__main__':
    df = ef.stock.get_quote_history(stock_codes='002487', beg='20210701')
    strategy_01(df)
    print("=======")
