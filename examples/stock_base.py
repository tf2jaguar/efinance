#!/usr/bin/python
# -*- coding: utf-8 -*-
def is_st_stock(_stock_name):
    """
    是否为ST及其他具有退市标签的股票
    Parameters
    ----------
    _stock_name 股票名称

    Returns 是否为ST及其他具有退市标签的股票
    -------

    """
    return 'ST' in _stock_name or \
           '*' in _stock_name or \
           '退' in _stock_name


def is_suspended_stock(_stock_price):
    """
    是否为停牌股票
    Parameters
    ----------
    _stock_code 股票代码

    Returns 是否为停牌股票
    -------

    """
    return '-' in str(_stock_price)


def is_gem_stock(_stock_code):
    """
    是否为创业版股票
    Parameters
    ----------
    _stock_code 股票代码

    Returns 是否为创业版股票
    -------

    """
    return _stock_code.startswith('30')


def is_star_stock(_stock_code):
    """
    是否为科创版股票
    Parameters
    ----------
    _stock_code 股票代码

    Returns 是否为科创版股票
    -------

    """
    return _stock_code.startswith('688')


def filter_stock(_row):
    _name = getattr(_row, '股票名称')
    _code = getattr(_row, '股票代码')
    _price = getattr(_row, '最新价')
    return is_st_stock(_name) or is_suspended_stock(_price) or is_gem_stock(_code) or is_star_stock(_code)
