'''
Created on Aug 22, 2014

@author: TPB
'''


import time, datetime

class ezTime(object):
    def __init__(self):
        self.tstart = 0
        self.tlast = 0
        self.tcurr = 0
        self.reset()
        self.min = 60
        self.hour = self.min * 60
        self.day = self.hour * 24
        self.week = self.day * 7
        
    def getDelta(self):
        self.tcurr = time.clock()
        delta = self.tcurr - self.tlast
        self.tlast = self.tcurr
        return delta
    
    def getTotal(self):
        return time.clock() - self.tstart
    
    def reset(self):
        self.tstart = time.clock()
        self.tlast = self.tstart
        
    def getTimeDate(self, sep = '/'):
        t = datetime.datetime.now()
        currdatetime = t.timetuple()
        yr = str(currdatetime[0])
        curr_date = "%02d%s"%(int(yr[2:]), sep) + "%02d%s"%(currdatetime[1], sep) + "%02d"%currdatetime[2]
        curr_time = "%02d:"%currdatetime[3] + "%02d:"%currdatetime[4] + "%02d"%currdatetime[5]
        tstamp = curr_date + "-" + curr_time
        return tstamp
    def getEPtime(self):
        return time.time() - time.timezone
    def getDate(self, sep):
        ds = self.getTimeDate(sep)
        return ds.split(' ')[0]
    def getTime(self):
        ts = self.getTimeDate()
        return ts.split(' ')[1]
    def getValue(self):
        return self.getTimeDate()
    
def checkDecimal(self, decimalString):
    self.logger.debug('Decimal Check attempt on %s' %decimalString)
    checkstr = decimalString.split('.')
    for part in checkstr:
        if  part.isdigit() == False:
            self.logger.error('Decimal Check Failed on %s in %s' %(part, decimalString))
            return False
    else:
        return True    
    
def getTS():
    """ get current date and time from system clock
    """
    t = datetime.datetime.now()
    currdatetime = t.timetuple()
    yr = str(currdatetime[0])
    curr_date = "%02d/"%int(yr[2:]) + "%02d/"%currdatetime[1] + "%02d"%currdatetime[2]
    curr_time = "%02d:"%currdatetime[3] + "%02d:"%currdatetime[4] + "%02d"%currdatetime[5]
    tstamp = curr_date + " " + curr_time
    return tstamp

def ts2pytime(ts):
    for i in range(len(ts)):
        ts[i]=ts2epoch(ts[i])
    return ts
        
def ts2epoch(ts):
    form = '%y/%m/%d %H:%M:%S'
    res = int(time.mktime(time.strptime(ts, form))) - time.timezone
    return res