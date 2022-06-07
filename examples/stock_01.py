import datetime

from tqdm import tqdm

import efinance as ef


def volume_bigger_in5(_cur_code, _cur_day, _cur_turnover, _cur_price):
    """
    放量。当前天交易量比之前5个交易日的交易量都大
    """
    beg_time = previous_work_day(_cur_day, 6).strftime('%Y%m%d')
    end_time = (datetime.datetime.strptime(_cur_day, '%Y%m%d') + datetime.timedelta(days=-1)).strftime('%Y%m%d')
    _df = ef.stock.get_quote_history(stock_codes=_cur_code, beg=beg_time, end=end_time)
    if _df.empty:
        return False
    # 大于前一天收盘价 或 大于前一天开盘价
    is_up = _df.iloc[-1, 4] <= _cur_price or _df.iloc[-1, 3] < _cur_price
    match_day_num = _df['成交量'][_df['成交量'] * 1.666 < _cur_turnover].count()
    if is_up and match_day_num > len(_df) - 2:
        return True
    else:
        return False


def previous_work_day(_cur_day, _previous):
    cur_day = datetime.datetime.strptime(_cur_day, '%Y%m%d')
    while _previous > 0:
        cur_day += datetime.timedelta(days=-1)
        # 一二 三四五 六七
        # 0 1 2 3 4 5 6
        if cur_day.weekday() < 5:
            _previous -= 1
    return cur_day


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
    matched = []
    today = datetime.datetime.now().strftime('%Y%m%d')
    for row in tqdm(_stocks.itertuples(), total=_stocks.shape[0]):
        if filter_stock(row):
            continue
        try:
            if volume_bigger_in5(getattr(row, '股票代码'), today, getattr(row, '成交量'), getattr(row, '最新价')):
                matched.append(getattr(row, '股票代码'))
        except Exception as e:
            print("except: %s-%s" % (getattr(row, '股票代码'), getattr(row, '股票名称')), e)
    return matched


def str_of_num(num):
    """
    递归实现，精确为最大单位值 + 小数点后三位
    Parameters
    ----------
    num

    Returns
    -------

    """

    def strofsize(num, level):
        if level >= 2:
            return num, level
        elif num >= 10000:
            num /= 10000
            level += 1
            return strofsize(num, level)
        else:
            return num, level

    units = ['', '万', '亿']
    num, level = strofsize(num, 0)
    if level > len(units):
        level -= 1
    return '{}{}'.format(round(num, 3), units[level])


if __name__ == '__main__':
    all_stock = ef.stock.get_realtime_quotes('沪深A股')
    matched_stock = strategy_01(all_stock)
    print("=======")
    print('len:', len(matched_stock), matched_stock)

    base_info = ef.stock.get_base_info(matched_stock)
    # print(ma)
    for sto in base_info.itertuples():
        print(getattr(sto, '股票代码'), getattr(sto, '股票名称'), str_of_num(getattr(sto, '总市值')))

    # today = datetime.datetime.now().strftime('%Y%m%d')
    # print(volume_bigger_in5('688120',today,1))
