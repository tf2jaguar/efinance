#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import multiprocessing as mp

import efinance as ef
from efinance.utils import money, date_time


def volume_bigger_in5(_cur_day, _stocks):
    """
    放量。当前天交易量比之前5个交易日的交易量都大
    """
    if filter_stock(_stocks):
        return None

    _cur_code = _stocks[0]
    _cur_turnover = _stocks[11]
    _cur_price = _stocks[3]
    print("process {} {} {}".format(_stocks[0], _stocks[1], _stocks[3]))

    beg_time = date_time.previous_work_day(_cur_day, 6).strftime('%Y%m%d')
    end_time = (datetime.datetime.strptime(_cur_day, '%Y%m%d') + datetime.timedelta(days=-1)).strftime('%Y%m%d')
    _df = ef.stock.get_quote_history(stock_codes=_cur_code, beg=beg_time, end=end_time)
    if _df.empty:
        return None
    # 大于前一天收盘价 或 大于前一天开盘价
    is_up = _df.iloc[-1, 4] <= _cur_price or _df.iloc[-1, 3] < _cur_price
    match_day_num = _df['成交量'][_df['成交量'] * 1.666 < _cur_turnover].count()
    if is_up and match_day_num > len(_df) - 2:
        return _cur_code
    else:
        return None


def is_st_stock(_stock_name):
    """
    过滤ST及其他具有退市标签的股票
    Parameters
    ----------
    _stock_name

    Returns
    -------

    """
    return 'ST' in _stock_name or \
           '*' in _stock_name or \
           '退' in _stock_name


def is_suspended_stock(_stock_price):
    return '-' in str(_stock_price)


def is_gem_stock(_stock_code):
    return _stock_code.startswith('30')


# 过滤科创版股票
def is_star_stock(_stock_code):
    return _stock_code.startswith('688')


def filter_stock(_row):
    _name = getattr(_row, '股票名称')
    _code = getattr(_row, '股票代码')
    _price = getattr(_row, '最新价')
    return is_st_stock(_name) or is_suspended_stock(_price) or is_gem_stock(_code) or is_star_stock(_code)


def strategy_01(_stocks):
    start_t = datetime.datetime.now()
    _num_cores = int(mp.cpu_count())
    print("use {} cpu calculate stock's ".format(_num_cores))

    pool = mp.Pool(_num_cores)
    today = datetime.datetime.now().strftime('%Y%m%d')
    results = [pool.apply_async(volume_bigger_in5, args=(today, _stocks.iloc[i, :])) for i in range(len(_stocks.index))]
    results = [p.get() for p in results]

    end_t = datetime.datetime.now()
    elapsed_sec = (end_t - start_t).total_seconds()
    print("multi-process calculation cost: {}s".format("{:.2f}".format(elapsed_sec)))
    return list(filter(None, results))


def run():
    all_stock = ef.stock.get_realtime_quotes('沪深A股')
    matched_stock = strategy_01(all_stock)
    print('len:', len(matched_stock), matched_stock)

    base_info = ef.stock.get_base_info(matched_stock)
    # print(ma)
    for sto in base_info.itertuples():
        print(getattr(sto, '代码'), getattr(sto, '名称'), money.str_of_num(getattr(sto, '总市值')))


if __name__ == '__main__':
    run()
