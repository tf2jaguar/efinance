#!/usr/bin/python
# -*- coding: utf-8 -*-
import efinance as ef
import stock_strategy_01 as strategy01
from efinance.utils import money


def run():
    all_stock = ef.stock.get_realtime_quotes('沪深A股')
    matched_stock = strategy01.strategy(all_stock)
    print('len:', len(matched_stock), matched_stock)

    base_info = ef.stock.get_base_info(matched_stock)
    # print(ma)
    for sto in base_info.itertuples():
        print(getattr(sto, '代码'), getattr(sto, '名称'), money.str_of_num(getattr(sto, '总市值')))


if __name__ == '__main__':
    run()
