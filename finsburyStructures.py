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
        '''
        overloading equality operator for object with __slots__
        '''
        if isinstance(other, self.__class__):
            for f in self.__slots__:
                if not (hasattr(self,f) == hasattr(self,f)):
                    return False
                elif hasattr(self,f) and not getattr(self,f) == getattr(other,f):
                    return False
            return True
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
        '''
        aggregate data by brand, cache result to self
        @return aggregated dict with brand as key, count as val
        '''
        if not hasattr(self,'aggregated'):
            self.aggregated = defaultdict(int)
            for d in self.data:
                self.aggregated[d.brand] += d.nSold
                
        return self.aggregated
    
    def getTopAggregatedBrands(self,N):
        '''
        get the top brands in terms of quantity sold by aggregating then sorting
        @param[in] N max number of results to return        
        @return topList list of the top brands in form [(brand, quantity),..]
        '''
        blist = [(b,v) for b,v in self.getAggregatedBrandQuantities().iteritems()]
        top = sorted(blist,key=lambda x:x[1],reverse=True)
        return top[:min(len(self.aggregated),N)]
    
    def getBottomAggregatedBrands(self,N):
        '''
        get the bottom brands in terms of quantity sold by aggregating then sorting
        @param[in] N max number of results to return        
        @return bottomList list of the top brands in form [(brand, quantity),..]
        '''
        blist = [(b,v) for b,v in self.getAggregatedBrandQuantities().iteritems()]
        bottom = sorted(blist,key=lambda x:x[1],reverse=False)
        return bottom[:min(len(self.aggregated),N)]    
    
    def getTotalProfit(self):
        '''
        get sum of profits over all items     
        @return totalProfit int in pence
        '''
        profits = [x.profit for x in self.data]
        return sum(profits)
        
    def getTopNProfits(self,N):
        '''
        get ordered list of the best N products by profit
        @param[in] N max number of results to return        
        @return topList list of the top StockInfo objects
        '''        
        topN = sorted(self.data,key=lambda x:x.profit,reverse=True)
        return topN[:min(self.n,N)]
    
    def getBottomNProfits(self,N):
        '''
        get ordered list of the worst N products by profit
        @param[in] N max number of results to return        
        @return topList list of the top StockInfo objects
        '''        
        topN = sorted(self.data,key=lambda x:x.profit)
        return topN[:min(self.n,N)]
    
    def getTopNQuantities(self,N):
        '''
        get ordered list of the best N products by quantity
        @param[in] N max number of results to return        
        @return topList list of the top StockInfo objects
        '''        
        topN = sorted(self.data,key=lambda x:x.nSold,reverse=True)
        return topN[:min(self.n,N)]
        
    def getBottomNQuantities(self,N):
        '''
        get ordered list of the worst N products by quantity
        @param[in] N max number of results to return        
        @return topList list of the top StockInfo objects
        '''        
        topN = sorted(self.data,key=lambda x:x.nSold)
        return topN[:min(self.n,N)]       
        
        
    

