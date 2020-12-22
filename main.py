import requests
import time

import Db


def getTimestamp():
    return int(round(time.time() * 1000))


def getTimeString():
    string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(getTimestamp() / 1000))
    return string


def insertStockAll(cursor, params=()):
    cursor.execute("INSERT IGNORE INTO stock_all (code, name, gmt_create) VALUES (?, ?, ?)", params)


if __name__ == '__main__':
    # https://55.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=5000&po=0&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f12&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1608605021839

    Db.initConnection()

    ts = getTimestamp()

    url = 'https://55.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=5000&po=0&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281' \
          '&fltt=2&invt=2&fid=f12&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,' \
          'f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_={}'.format(ts)
    resp = requests.get(url)
    if resp.status_code == 200:
        stockJson = resp.json()
        rc = stockJson['rc']
        if rc == 0:
            data = stockJson['data']
            diff = data['diff']
            for idx in range(len(diff)):
                item = diff[idx]
                if item['f13'] == 0:
                    prefix = 'sz'
                else:
                    prefix = 'sh'
                code = '{}{}'.format(prefix, item['f12'])
                name = item['f14']
                Db.dbExecute(insertStockAll, (code, name, getTimeString()))

                # day k
                # https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SZ002027&begin=1608700670525&period=day&type=before&count=-36500&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance
                codeUpper = code.upper()
                detailUrl = 'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={}&begin={' \
                            '}&period=day&type=before&count={}&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,' \
                            'balance'.format(codeUpper, getTimestamp(), -36500)
                detailResp = requests.get(detailUrl)
                if detailResp.status_code == 200:
                    detailJson = detailResp.json()
                    pass
                else:
                    print('{} get failed'.format(detailUrl))
        else:
            print('list stock get failed.')
    else:
        print('{} get failed.'.format(url))
