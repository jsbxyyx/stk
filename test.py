from datetime import datetime

import Db
from StockDao import StockDao

if __name__ == '__main__':
    lastDatetime = datetime.strptime('2020-12-22', '%Y-%m-%d')
    lmt = abs((datetime.now() - lastDatetime).days)
    print('lmt = {}'.format(lmt))

    Db.initConnectionPool()

    klineInfo = Db.dbExecute(StockDao.selectLastKlineByCode, ('0.000001',))
    print('date = {}'.format(klineInfo.date))
