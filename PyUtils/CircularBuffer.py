'''
Created on Aug 22, 2014

@author: TPB
'''

import time
import pickle
from PyUtils.DebugLog import TBLogger

import GlobalConfig


#logging
circbuffrootlog = TBLogger(GlobalConfig.logpath+__name__+'.out','info','Cbuff')

class data_buffer(object):

    def __init__(self,keys,size,path,name):
        self.name = name
        self.logger = circbuffrootlog.MakeChild(self.name + '_Buffer')
        self.pname = name + '.pickle'
        self.save_path = path + self.pname
        self.max = size
        self.min = 0
        self.keys = keys
        self.FlushBuffer()
        self.timecutoff = {'All':(3600*24*90), #up to 90 days in the past - so not really all, but should be pretty close
                        'Month':(3600*24*30), #30 days previous
                        'Week':(3600*24*7), #etc
                        'Day':(3600*24),
                        '4 Hour':(3600*4),
                        'Hour':3600}
    
    def saveBuffer(self,path = None ,mode = 'wb'):
        if not path: path = self.save_path
        pickle.dump(self.buff, open(path,mode) ,protocol = 2)
    
    def loadBuffer(self, keys = None , store = False):
        if not keys: keys = self.keys
        try:
            data = pickle.load(open(self.save_path,'rb'))
        except EOFError:
            #empty pickle file, load blank dict
            return dict.fromkeys(keys)
        ret_data = dict.fromkeys(keys)
        data_len = int()
        for key in ret_data:
            ret_data[key] = data[key]
            data_len = len(data[key])
        if store:
            self.FlushBuffer()
            if self.checkRelevance(ret_data):
                self.logger.error( 'Relevant data found!!')
                self.buff = ret_data
            else: self.logger.error('Data in file %s not relevant' %self.name)
        self.logger.debug('%s data points read into buffer from %s' %(data_len, self.name))
        return ret_data        
    
    def checkRelevance(self,data = None):
        if not data: data = self.buff
        now = time.time() - time.timezone
        self.logger.debug('Newest Data Point - Now = %s' %(now - data['Epoch Time'][-1]))
        if (now - data['Epoch Time'][-1]) > self.timecutoff[self.name]:
            return True
        else:
            return False
        

    def returnKeys(self,keys):
        ret_dict = dict.fromkeys(keys)
        for key in ret_dict:
            ret_dict[key] = self.buff[key]
        return ret_dict
    
    def Write(self,data):
        for key in self.buff:
            if not self.isFull():
                self.buff[key].append(data[key])
            elif self.isFull():
                self.buff[key].pop(0)
                self.buff[key].append(data[key])

        
    def ReadAvg(self,window = 4, index = -1):
    
        avg_dict = dict.fromkeys(self.keys)
        
        for key in self.buff:
            avg_dict[key]=list()
            if type(self.buff[key][-1]) == int: 
                avg_dict[key] = sum(self.buff[key][-window:])/float(window)
            elif type(self.buff[key][-1]) == float: 
                avg_dict[key] = sum(self.buff[key][-window:])/float(window)
            elif type(self.buff[key][-1]) == str: 
                avg_dict[key]=self.buff[key][-(window/2)]
            elif type(self.buff[key][-1]) == tuple: 
                tuplen = len(self.buff[key][-1])
                sized_list = list()
                for i in range(tuplen):
                    sized_list.append(0)
                avg_dict[key] = sized_list
                for i in range(tuplen):    #iterate over length of tuple
                    for win in range(window):
                        avg_dict[key][i] += self.buff[key][-win][i]
                avg_dict[key][i] = avg_dict[key][i]/float(window)
        return avg_dict
    
    
    def getBufferSize(self, return_dict = False):
        ret_dict = dict.fromkeys(self.keys)
        for key in self.buff:
            buflen = len(self.buff[key])
            ret_dict[key] = buflen
        if return_dict: return ret_dict
        else: return ret_dict.values()[0]
    
    def isFull(self):
        #ret_dict = dict.fromkeys(self.keys)
        for key in self.buff:
            if len(self.buff[key]) == self.max: 
                return True
            else: return False
    
    def isEmpty(self):
        #ret_dict = dict.fromkeys(self.keys)
        for key in self.buff:
            if len(self.buff[key]) == self.min: 
                return True
            else: return False

    def FlushBuffer(self):
        self.buff = dict.fromkeys(self.keys)
        for key in self.buff:
            self.buff[key] = list()
                
class circ_buffer(object):
    def __init__(self, size = 120):
        self.buff = list()
        self.max = size

    def cbisFull(self):
        if len(self.buff) == self.max:
            return True
        else: return False
        
    def cbisEmpty(self):
        if len(self.buff) == 0:
            return True
        else: return False
    
    def cbWrite(self,data):        
        if not self.cbisFull():
            self.buff.append(data)
        elif self.cbisFull():
            self.buff.pop(0)
            self.buff.append(data)
    def cbFlushBuffer(self):
        self.buff = list()
        
    def cbReadAvg(self,window = 4,index = -1):
        if type(self.buff[-1]) == int:
            #print('Buffer Entry = Int')
            avg = sum(self.buff[-window:])/float(window)
            return avg
            
        elif type(self.buff[-1]) == dict:
            #print('Buffer Entry = Dict')
            avg = dict.fromkeys(self.buff[-1].keys())
            for key,val in self.buff[-1].iteritems():
                if type(val) == int:
                    #print('Value Entry = Int')
                    avg[str(key)] = 0
                elif type(val) == float:
                    #print('Value Entry = Float')
                    avg[str(key)] = 0
                elif type(val) == str:
                    #print('Value Entry = String')
                    avg[str(key)] = str()
                elif type(val) == tuple:
                    #print('Value Entry = Tuple')
                    avg[str(key)] = [0,0,0]
                    
            for i in range(window):
                for key,val in self.buff[-window+i].iteritems():
                    ##print 'Index: %s Key: %s Val: %s Type: %s' %(i, key, val, type(val))
                    if type(val) == int:
                        avg[str(key)] += val
                    elif type(val) == float:
                        avg[str(key)] += val
                    elif type(val) == str:
                        pass
                    elif type(val) == tuple:
                        avg[str(key)] = [avg[str(key)][0] +val[0],avg[str(key)][1] + val[1],avg[str(key)][2]+val[2]]
                        ##print 'Avg: %s Key: %s Val: %s Type: %s' %(i, key, avg[str(key)], type(avg[str(key)]))
            for key in avg:
                    if type(avg[str(key)]) == int:
                        avg[str(key)] = avg[str(key)]/float(window)
                    elif type(avg[str(key)]) == float:
                        avg[str(key)] = avg[str(key)]/float(window)
                    elif type(avg[str(key)]) == str:
                        avg[str(key)]=self.buff[-(window/2)][key]
                    elif type(avg[str(key)]) == list:   
                        ##print avg[str(key)]             
                        avg[str(key)]  = (avg[str(key)][0]/float(window),avg[str(key)][1]/float(window),avg[str(key)][2]/float(window))
            return avg
        else:
            pass#print("WTF")