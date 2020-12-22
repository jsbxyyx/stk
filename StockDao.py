from EastmoneyKlineInfo import EastmoneyKlineInfo


class StockDao(object):

    def __init__(self):
        pass

    @staticmethod
    def insertStockAll(cursor, params=()):
        """ Insert stock all record """
        cursor.execute('INSERT IGNORE INTO stock_all (code, name, gmt_create) VALUES (?, ?, ?)', params)

    @staticmethod
    def insertStockKline(cursor, params=()):
        """ Insert stock kline record"""
        cursor.execute(
            'INSERT IGNORE INTO stock_kline (date, code, open, close, high, low, volume, turnover, amplitude, '
            'change_rate, change_amount, turnover_rate) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', params)

    @staticmethod
    def selectLastKlineByCode(cursor, params=()):
        """ Select last kline record by code """
        cursor.execute('SELECT id, date, code, open, close, high, low, volume, turnover, amplitude, change_rate, '
                       'change_amount, turnover_rate FROM stock_kline t WHERE t.code = ? ORDER BY t.date DESC LIMIT '
                       '1', params)
        klineInfo = None
        for (id, date, code, open, close, high, low, volume, turnover,
             amplitude, change_rate, change_amount, turnover_rate) in cursor:
            klineInfo = EastmoneyKlineInfo(id, code, date, open, close, high, low, volume, turnover, amplitude,
                                           change_rate,
                                           change_amount, turnover_rate)
        return klineInfo
