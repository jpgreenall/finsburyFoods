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
    __slots__ = ['ean','name','brand','quantity','wholesalePr','sellthroughPr',
                 'batchsize','nSold','margin','profit']
    priceFieldname={'standard-sellthrough':'sellthroughPr','wholesale':'wholesalePr'}
    def __init__(self,**kwargs):
        for key,val in kwargs.iteritems():
            setattr(self,key,val)
        return
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            same = True
            for f in self.__slots__:
                if not getattr(self,f) == getattr(other,f):
                    same = False
            return same
        else:
            return False
    
    def __ne__(self, other):
        return not self.__eq__(other)    
    

