#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import json
import multiprocessing as mp
import os

import efinance as ef
from efinance.utils import notify
from efinance.utils import rsi


def get_etf_dict_list(_etf_dict):
    return [str(_etf_dict['code']), str(_etf_dict['name']), str(_etf_dict['type_name']), str(_etf_dict['org_name']),
            str(_etf_dict['rsi'])]


def cur_rsi(_code):
    _rsi = [0, 0]
    day_k = ef.stock.get_quote_history(_code)
    day_256_k = day_k['收盘'][-256:]
    try:
        if len(day_256_k) == 0:
            return _rsi
        elif len(day_256_k) > 255:
            _rsi = rsi.smooth_rsi(day_256_k, 28)
        else:
            _rsi = rsi.smooth_rsi(day_256_k, 28, True)
    except Exception as e:
        print("exception", _code)
        pass
        return _rsi
    return _rsi


def below_rsi(etf_dict, max_rsi):
    _rsi = cur_rsi(etf_dict['code'])
    print(etf_dict['code'], etf_dict['name'], _rsi[-2:])

    if 0 < _rsi[-1] < max_rsi:
        etf_dict['rsi'] = _rsi[-1]
        return ", ".join(get_etf_dict_list(etf_dict)) + "\n"
    return None


def multi_process_match_rsi(funds_dict, rsi):
    start_t = datetime.datetime.now()
    _num_cores = int(mp.cpu_count())
    print("use {} cpu calculate etf's rsi below {}".format(_num_cores, rsi))

    pool = mp.Pool(_num_cores)
    results = [pool.apply_async(below_rsi, args=(fund, rsi)) for fund in funds_dict]
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
    # run_by_config()
    all_funds = ef.fund.get_fund_codes(ft='etf')
    for co in all_funds:
        print(co)
