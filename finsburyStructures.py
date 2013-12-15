'''
This file contains the class definition for data structures used by Finsbury Foods

@author : John Greenall
@date : 15-12-2013
'''

class StockInfo(object):
    '''
    simple class used to hold stock info
    use __slots__ to maximize efficiency of storage
    '''
    __slots__ = ['ean','name','brand','quantity','wholesalePr','sellthroughPr','batchsize','nSold']
    def __init__(self,**kwargs):
        for key,val in kwargs.iteritems():
            setattr(self,key,val)
        return
    

