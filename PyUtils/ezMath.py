'''
Created on Aug 22, 2014

@author: TPB
'''

def oddround(fnum):
    ans = int(round(fnum))
    if ans %2:
        return ans
    else: return ans -1
    
def evenround(fnum):
    return int(round(fnum/2.)*2)