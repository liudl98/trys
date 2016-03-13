import csv
import os.path
from datetime import datetime, timedelta
from yahoo_finance import Share

def get_data(symbol='^GSPC'):
    symbol1 = symbol
    if symbol1[0] == '^':
        symbol1 = symbol[1:]
   
    fileName = 'c:/data/%s.csv' % symbol1
    keys = ['Date', 'Close']  # only save these fields
    
    gspc = Share(symbol)
    if os.path.isfile(fileName):
        result = read_data(fileName)
        oneday = timedelta(1)
        yesterday = datetime.today().date() - oneday
        latest = datetime.strptime(result[0]['Date'], '%Y-%m-%d').date()+oneday
        if latest < yesterday:
            print('Extending from %s to %s ...' % (str(latest), str(yesterday)))
            result = gspc.get_historical(str(latest), str(yesterday)) + result
            write_data(fileName, result, keys)
        else:
            print('No need to update')
    else:
        result = gspc.get_historical('1976-02-01', '2016-02-21')
        write_data(fileName, result, keys)

    return result
    
def read_data(fileName):
    result = []
    data = list(csv.reader(open(fileName)))
    keys = data[0]
    for row in data[1:]:
        result.append(dict(zip(keys, row)))
        
    return result
    
def write_data(fileName, result, keys):
    keys = sorted(keys)
    w = csv.writer(open(fileName, 'w'), lineterminator='\n')
    w.writerow(list(keys))
    for item in result:
        w.writerow([item.get(k) for k in keys])
            
 
def convert_data(fileName):
    result = read_data(fileName)
    keys = ['Date', 'Close']  # only save these fields
    write_data(fileName, result, keys)
 
if __name__ == '__main__':
    get_data()
#     convert_data('c:/data/GSPC.csv')