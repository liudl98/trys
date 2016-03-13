from get_data import get_data
import matplotlib.pyplot as plt
import numpy as np
import datetime

def main():
    years = range(1976, 2016)
    data = get_data()[::-1]  # reverse so the latest data is last
    dates = [datetime.datetime.strptime(a['Date'], '%Y-%m-%d') 
             for a in data]
    annDates = [datetime.datetime(y, 2, 1) for y in years]
    indexes = []
    k = 0
    for d in annDates:
        for k1, d1 in enumerate(dates[k:]):
            if d1 >= d:
                k += k1
                indexes.append(k)
                break
    
    n = len(indexes) - 1
    rates = []
    for i in range(n):
        k0 = indexes[i]
        k1 = indexes[i+1]
        bgnVal = float(data[k0]['Close'])
        bgnDate = data[k0]['Date']
        endVal = float(data[k1]['Close'])
        endDate = data[k1]['Date']
        ret = (endVal - bgnVal) / bgnVal * 100
        ret1 = min(4.75, max(0, ret))
        rates.append((ret, ret1))
        print('From %s to %s [%d to %d], %.2f to %.2f: %.2f' % 
              (bgnDate, endDate, k0, k1, bgnVal, endVal, ret1))

    print('Full returns: %.2f, %.2f' % accRates(rates, 0, n-1))
    
    x = []
    y1 = []
    y2 = []
    for i in range(n-10):
        acc = accRates(rates, i, i+10)
        print('Between %r and %r: (%.2f, %.2f)' % 
              (annDates[i].strftime('%Y-%m-%d'), 
               annDates[i+10].strftime('%Y-%m-%d'), acc[0], acc[1]))
        year = annDates[i].year
        x.append(year)
        y1.append(acc[0])
        y2.append(acc[1])

    x = np.array(x)
    y1 = np.array(y1)
    y2 = np.array(y2)
               
    fig = plt.figure()
    axes = fig.add_subplot(111)
    axes.plot(x, y1, '*-')
    axes.hold('on')
    axes.plot(x, y2, '*-')
    plt.title('%.2f vs %.2f' % (y1.mean(), y2.mean()))
    plt.grid('on')
    
    plt.show()
    
    
def accRates(rates, bgnIndex, endIndex):
    fullRate = 1
    annRate = 1
    for k in range(bgnIndex, endIndex+1):
        r = rates[k]
        fullRate = fullRate * (1 + r[0] / 100)
        annRate = annRate * (1 + r[1] / 100)
    fullRate = (fullRate - 1) * 100
    annRate = (annRate - 1) * 100
    return (fullRate, annRate)

if __name__ == '__main__':
    main()