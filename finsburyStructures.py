'''
This file contains the class definition for data structures used by Finsbury Foods

@author : John Greenall
@date : 15-12-2013
'''
from collections import defaultdict

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
    
class StockInfoList:
    '''
    class that just contains helper functions for sorting and aggregating a list
    of StockInfo Objects
    '''
    def __init__(self,stockList):
        self.data = stockList
        self.n = len(self.data)
        
    def getAggregatedBrandQuantities(self):
        if not hasattr(self,'aggregated'):
            self.aggregated = defaultdict(int)
            for d in self.data:
                self.aggregated[d.brand] += d.nSold
                
        return self.aggregated
    
    def getTopAggregatedBrands(self,N):
        blist = [(b,v) for b,v in self.getAggregatedBrandQuantities().iteritems()]
        top = sorted(blist,key=lambda x:x[1],reverse=True)
        return top[:min(len(self.aggregated),N)]
    
    def getBottomAggregatedBrands(self,N):
        blist = [(b,v) for b,v in self.getAggregatedBrandQuantities().iteritems()]
        top = sorted(blist,key=lambda x:x[1],reverse=False)
        return top[:min(len(self.aggregated),N)]    
    
    def getTotalProfit(self):
        profits = [x.profit for x in self.data]
        return sum(profits)
        
    def getTopNProfits(self,N):
        topN = sorted(self.data,key=lambda x:x.profit,reverse=True)
        return topN[:min(self.n,N)]
    
    def getBottomNProfits(self,N):
        topN = sorted(self.data,key=lambda x:x.profit)
        return topN[:min(self.n,N)]
    
    def getTopNProfits(self,N):
            topN = sorted(self.data,key=lambda x:x.profit,reverse=True)
            return topN[:min(self.n,N)]
        
    def getBottomNProfits(self,N):
        topN = sorted(self.data,key=lambda x:x.profit)
        return topN[:min(self.n,N)]       
        
        
    

