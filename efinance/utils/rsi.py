"""
 LC := REF(CLOSE,1);   // 前一天收盘价
 RSI$1:SMA(MAX(CLOSE-LC,0),N1,1)/SMA(ABS(CLOSE-LC),N1,1)*100; // N1周期的rsi
"""
import numpy as np


def get_sma(c, n, m):
    """
    sma函数；c/列表，n/周期，m/权重，返回sma列表
    :param c: 列表
    :param n: 周期
    :param m: 权重
    :return: sma列表
    """
    c_re = []
    m_n = m / n
    m_n2 = 1 - m_n
    sma_temp = c[0]
    c_re.append(sma_temp)
    for i in range(1, len(c)):
        sma_temp = c[i] * m_n + sma_temp * m_n2
        c_re.append(sma_temp)
    return c_re


def smooth_rsi(t, n, is0=False):
    """
    平滑rsi函数；输入一个列表和周期，返回rsi列表
    :param t: 列表
    :param n: 周期
    :param is0: is0为True的时候，将首个值赋0，序列少的时候使用
    :return: rsi列表
    """
    close = list(t)[1:]
    lc = list(t)[:-1]
    close_lc = np.array(close) - np.array(lc)
    if not is0:
        close_lc1 = np.maximum(close_lc, 0)  # MAX(CLOSE-LC,0)
        close_lc2 = abs(close_lc)  # ABS(CLOSE-LC)
    else:
        close_lc1 = [0] + list(np.maximum(close_lc, 0))  # MAX(CLOSE-LC,0)
        close_lc2 = [0] + list(abs(close_lc))  # ABS(CLOSE-LC)
    close_lc_s = get_sma(close_lc1, n, 1)  # SMA(MAX(CLOSE-LC,0),N1,1)
    close_lc2_s = get_sma(close_lc2, n, 1)  # SMA(ABS(CLOSE-LC),N1,1)
    # 考虑了分母是0，分子和分母都是0的情况
    divisor = np.array(close_lc_s) * 100
    dividend = np.array(close_lc2_s)
    t_rsi = [round(e_temp, 2) if e_temp != np.inf and not np.isnan(e_temp) else 0
             for e_temp in np.divide(divisor, dividend, out=np.zeros_like(divisor), where=dividend != 0)]
    return t_rsi
