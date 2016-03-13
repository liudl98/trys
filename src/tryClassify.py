from get_data import get_data
from datetime import datetime


def main():
    data = get_data()
    data = data[::-1]
    data_len = len(data)
    weekDayName = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    closeVals = [float(d['Close']) for d in data]
    
    changes = [(closeVals[i+1]/closeVals[i]-1) * 100
               for i in range(data_len-1)]
    
    dates = [datetime.strptime(data[i]['Date'], '%Y-%m-%d').date()
               for i in range(data_len-1)]
    
    for i in range(data_len-10, data_len-1):
        print('%s (%s): %s==>%s, %.2f' % (dates[i], weekDayName[dates[i].weekday()], 
                                     closeVals[i], closeVals[i+1], changes[i]))

    nTotal = [0] * 5
    nPos = [0] * 5
    for i in range(data_len-1):
        k = dates[i].weekday()
        nTotal[k] = nTotal[k] + 1
        if changes[i] > 0:
            nPos[k] = nPos[k] + 1
            
    for k in range(5):
        print('%s, nTotal=%d, nPos=%d (%.2f)' % 
              (weekDayName[k], nTotal[k], nPos[k], nPos[k] / nTotal[k] * 100))
            
if __name__ == '__main__':
    main()