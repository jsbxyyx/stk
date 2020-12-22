from EastmoneyKlineInfo import EastmoneyKlineInfo


class StockDao(object):

    def __init__(self):
        pass

    @staticmethod
    def sqlInsertStockAll():
        return 'INSERT IGNORE INTO stock_all (code, name, gmt_create) VALUES (?, ?, ?)'

    @staticmethod
    def insertStockAll(cursor, params=()):
        """ Insert stock all record """
        cursor.execute(StockDao.sqlInsertStockAll(), params)

    @staticmethod
    def sqlInsertStockKline():
        return 'INSERT IGNORE INTO stock_kline (date, code, open, close, high, low, volume, turnover, amplitude, ' \
            'change_rate, change_amount, turnover_rate) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

    @staticmethod
    def insertStockKline(cursor, params=()):
        """ Insert stock kline record"""
        cursor.execute(StockDao.sqlInsertStockKline(), params)

    @staticmethod
    def sqlSelectLastKlineByCode():
        return 'SELECT id, date, code, open, close, high, low, volume, turnover, amplitude, change_rate, ' \
                       'change_amount, turnover_rate FROM stock_kline t WHERE t.code = ? ORDER BY t.date DESC LIMIT 1'

    @staticmethod
    def selectLastKlineByCode(cursor, params=()):
        """ Select last kline record by code """
        cursor.execute(StockDao.sqlSelectLastKlineByCode(), params)
        klineInfo = None
        for (id, date, code, open, close, high, low, volume, turnover,
             amplitude, change_rate, change_amount, turnover_rate) in cursor:
            klineInfo = EastmoneyKlineInfo(id, code, date, open, close, high, low, volume, turnover, amplitude,
                                           change_rate, change_amount, turnover_rate)
        return klineInfo
