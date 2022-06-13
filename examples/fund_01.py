#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import json
import multiprocessing as mp
import os

import efinance as ef
from efinance.utils import notify
from efinance.utils import rsi


def strategy_below_rsi(fund_series, max_rsi):
    day_k = ef.stock.get_quote_history(fund_series[0])
    _rsi = rsi.cur_rsi(fund_series[0], day_k)
    print(fund_series[0], fund_series[1], _rsi[-2:])

    if 0 < _rsi[-1] < max_rsi:
        return ", ".join([str(fund_series[0]), str(fund_series[1]), str(_rsi[-1])]) + "\n"
    return None


def multi_process_match_rsi(_funds, _rsi):
    start_t = datetime.datetime.now()
    _num_cores = int(mp.cpu_count())
    print("use {} cpu calculate etf's rsi below {}".format(_num_cores, _rsi))

    pool = mp.Pool(_num_cores)
    results = [pool.apply_async(strategy_below_rsi, args=(_funds.iloc[i, :], _rsi)) for i in range(len(_funds.index))]
    results = [p.get() for p in results]

    end_t = datetime.datetime.now()
    elapsed_sec = (end_t - start_t).total_seconds()
    print("multi-process calculation cost: {}s".format("{:.2f}".format(elapsed_sec)))
    return list(filter(None, results))


def find_match_etf(_below_rsi=30, _send_notify=True):
    time_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M')
    all_funds = ef.fund.get_fund_codes(ft='etf')
    match_etf_list = multi_process_match_rsi(all_funds, _below_rsi)
    if not match_etf_list:
        match_etf_list.append('暂无匹配结果')

    if _send_notify:
        notify.send(time_prefix[:-4] + ' etf统计', ''.join(match_etf_list))
    return match_etf_list


def run_by_config():
    etf_strs = os.getenv('etf_config')
    if not etf_strs:
        etf_strs = '{"below_rsi":30, "send_notify":"True"}'
        print('calculate match etf has no etf_config! use default')
    etf_config = json.loads(etf_strs)

    find_match_etf(_below_rsi=etf_config['below_rsi'], _send_notify=eval(etf_config['send_notify']))
    print("calculate all user's work hours down.")


if __name__ == '__main__':
    run_by_config()
