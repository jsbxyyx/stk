# https://pypi.tuna.tsinghua.edu.cn/simple/
# install lib : requests, mariadb

import warnings

import requests
import time
from datetime import datetime

import Db
from StockDao import StockDao


def getTimestamp():
    return int(round(time.time() * 1000))


def getTimeString():
    string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(getTimestamp() / 1000))
    return string


if __name__ == '__main__':
    # https://55.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=5000&po=0&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f12&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1608605021839

    Db.initConnectionPool()
    stockDao = StockDao()

    ts = getTimestamp()

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'}

    url = 'https://55.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=5000&po=0&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281' \
          '&fltt=2&invt=2&fid=f12&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,' \
          'f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_={}'.format(ts)
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        stockJson = resp.json()
        if stockJson['rc'] == 0:
            data = stockJson['data']
            diff = data['diff']
            for i in range(len(diff)):
                iitem = diff[i]
                code_ = '{}.{}'.format(iitem['f13'], iitem['f12'])
                name = iitem['f14']
                Db.dbExecute(StockDao.insertStockAll, (code_, name, getTimeString()))

                klineInfo = Db.execute(StockDao.selectLastKlineByCode, (code_,))
                lmt = 36500
                if klineInfo is not None:
                    lastDatetime = datetime.strptime(klineInfo.date, '%Y-%m-%d')
                    lmt = abs((datetime.now() - lastDatetime).days)
                    if lmt == 0:
                        lmt = 1

                # day k
                # https://98.push2his.eastmoney.com/api/qt/stock/kline/get?secid=1.600686&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=0&end=20500101&lmt=120&_=1608617483343
                detailUrl = 'https://98.push2his.eastmoney.com/api/qt/stock/kline/get?secid={}.{}&ut' \
                            '=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52' \
                            '%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=0&end=20500101&lmt' \
                            '={}&_={}'.format(iitem['f13'], iitem['f12'], lmt, getTimestamp())
                detailResp = requests.get(detailUrl, headers=headers, verify=False)
                if detailResp.status_code == 200:
                    detailJson = detailResp.json()
                    if detailJson['rc'] == 0:
                        detailData = detailJson['data']
                        klines = detailData['klines']
                        paramsList = []
                        for j in range(len(klines)):
                            jitem = klines[j]
                            jitemSplit = jitem.split(',')
                            date_ = jitemSplit[0]
                            open_ = jitemSplit[1]
                            close_ = jitemSplit[2]
                            high = jitemSplit[3]
                            low = jitemSplit[4]
                            volume = jitemSplit[5]
                            turnover = jitemSplit[6]
                            amplitude = jitemSplit[7]
                            changeRate = jitemSplit[8]
                            changeAmount = jitemSplit[9]
                            turnoverRate = jitemSplit[10]
                            paramsList.append((date_, code_, open_, close_, high, low, volume,
                                               turnover, amplitude, changeRate, changeAmount,
                                               turnoverRate))
                            if len(paramsList) % 1000 == 0:
                                Db.batchUpdate(StockDao.sqlInsertStockKline(), paramsList)
                                paramsList.clear()
                        if len(paramsList) > 0:
                            Db.batchUpdate(StockDao.sqlInsertStockKline(), paramsList)
                            paramsList.clear()
                    else:
                        print('detail kline get failed. code : [{}]'.format(code_))
                else:
                    print('[{}] get failed'.format(detailUrl))
                print('code : {} OK'.format(code_))
        else:
            print('list stock get failed.')
    else:
        print('[{}] get failed.'.format(url))
