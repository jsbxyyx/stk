class EastmoneyKlineInfo(object):

    def __init__(self, id, code, date, open, close, high, low, volume, turnover, amplitude, changeRate, changeAmount, turnoverRate):
        # klines
        self.id = id  #
        self.code = code  # 股票代码
        self.date = date  # 日期
        self.open = open  # 开盘价
        self.close = close  # 收盘价
        self.high = high  # 最高
        self.low = low  # 最低
        self.volume = volume  # 成交量
        self.turnover = turnover  # 成交额
        self.amplitude = amplitude  # 振幅
        self.changeRate = changeRate  # 涨跌幅
        self.changeAmount = changeAmount  # 涨跌额
        self.turnoverRate = turnoverRate  # 换手率
