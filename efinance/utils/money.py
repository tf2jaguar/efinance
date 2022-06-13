def str_of_num(num):
    """
    递归实现，精确为最大单位值 + 小数点后三位
    """

    def s2n(_num, _level):
        if _level >= 2:
            return _num, _level
        elif _num >= 10000:
            _num /= 10000
            _level += 1
            return s2n(_num, _level)
        else:
            return _num, _level

    units = ['', '万', '亿']
    num, level = s2n(num, 0)
    if level > len(units):
        level -= 1
    return '{}{}'.format(round(num, 3), units[level])
