import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
from binance.error import ClientError
import time
import datetime
import platform

config_logging(logging, logging.DEBUG)

key = "B6s2D1QFv9UCHtCQ7bJxmwtZzAudRgUhHihHcLfWXshODWHwY0XRwPavZbrptYgD"
secret = "l7SF4MsU3nzXJIFxQ0xjofngASHmLza6LahZrhXtBW6XBzFddswMaE5BSxnz5GkD"

client = Client(key, secret)

print('Press enter to start')
a = input()
start = int(time.time()) * 1000

print('Press enter to stop')
b = input()
stop = int(time.time()) * 1000

day = datetime.datetime.now()

out_dir = 'files'

slash = '/'
if platform.system() == 'Windows':
    slash = '\\'

with open(out_dir + slash + str(day).split(sep='.')[0].replace(':', '.') + '.txt', 'w') as out:
    sum_buy = 0
    sum_sell = 0

    try:
        response = client.c2c_trade_history('BUY', startTimestamp=start, endTimestamp=stop)
        data = response['data']

        for i in data:
            if i['orderStatus'] == 'COMPLETED' and i['fiat'] == 'RUB':
                out.write('BUY ' + str(i['totalPrice']) + ' ' + time.ctime(i['createTime'] // 1000) + '\n')
                sum_buy += float(i['totalPrice'])

        response = client.c2c_trade_history('SELL', startTimestamp=start, endTimestamp=stop)
        data = response['data']

        for i in data:
            if i['orderStatus'] == 'COMPLETED':
                out.write('SELL ' + str(i['totalPrice']) + ' ' + time.ctime(i['createTime'] // 1000) + '\n')
                sum_sell += float(i['totalPrice'])

        out.write('\nOuto ' + str(sum_buy) + '\n' + 'Into ' + str(sum_sell) + '\n')
        out.write('Earned ' + str(sum_sell - sum_buy) + ' ' +
                  str(((sum_sell - sum_buy) / (sum_buy + 0.00001)) * 100) + '%\n')

    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )
