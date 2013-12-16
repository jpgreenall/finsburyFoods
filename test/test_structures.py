'''
This file contains unittests for Finsbury Foods

@author : John Greenall
@date : 15-12-2013
'''
import sys
import os
testFolder = os.path.split(os.path.realpath(__file__))[0]
baseFolder = os.path.split(testFolder)[0]
sys.path.append(baseFolder)
import finsburyStructures as structs
import unittest
import numpy

class FinsburyStructTester(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #build a list of Entries to test with
        self.nSold = [0,5,3,8,100,3]
        self.margin = [100,5,9,20,1,5]
        self.profit = [n*m for n,m in zip(self.nSold,self.margin)]
        self.stockList = structs.StockInfoList([structs.StockInfo(margin=m,nSold=n,profit=n*m,ean=str(e)) 
                          for e,(n,m) in enumerate(zip(self.nSold,self.margin))])
        
    def test_init(self):
        #make sure slots have been correctly set up to raise when non existent field used
        self.assertRaises(AttributeError,structs.StockInfo,nonExistentField=1)
        return
    
    def test_totalProfit(self):
        self.assertEqual(self.stockList.getTotalProfit(),sum(self.profit))
        return
    
    def test_getTopProfits(self):
        profitOrder = numpy.argsort(self.profit)[::-1].tolist()
        for n in [1,3,6]:
            topN = self.stockList.getTopNProfits(n)
            ean = [int(x.ean) for x in topN]
            self.assertListEqual(profitOrder[:n],ean)
        return
            
    def test_getBottomProfits(self):
        profitOrder = numpy.argsort(self.profit).tolist()
        for n in [1,3,6]:
            topN = self.stockList.getBottomNProfits(n)
            ean = [int(x.ean) for x in topN]
            self.assertListEqual(profitOrder[:n],ean)        
        
        return
    
    def test_getAggregatedBrandQuantitites(self):
        nSold =  [0,   1,  1,  2,  1,  2,  7,  4,  1,  3]
        brands = ['a','b','c','b','c','d','e','b','d','e']
        sol = {'a':0,'b':7,'c':2,'d':3,'e':10}
        brandList = structs.StockInfoList([structs.StockInfo(nSold=n,brand=b) 
                                           for n,b in zip(nSold,brands)])
        aggregated = brandList.getAggregatedBrandQuantities()
        self.assertDictEqual(sol,aggregated)
        
        top3 = [('e',10),('b',7),('d',3)]
        self.assertEqual(top3,brandList.getTopAggregatedBrands(3))
        
        bottom2 = [('a',0),('c',2)]
        self.assertEqual(bottom2,brandList.getBottomAggregatedBrands(2))
        bottom = [('a',0)]        
        self.assertEqual(bottom,brandList.getBottomAggregatedBrands(1))
        
        brands = len(nSold)*['a']
        brandList = structs.StockInfoList([structs.StockInfo(nSold=n,brand=b) 
                                                   for n,b in zip(nSold,brands)])
        #check we cope when only one brand        
        sumA = sum(nSold)     
        sol = {'a':sumA}
        aggregated = brandList.getAggregatedBrandQuantities()
        self.assertDictEqual(sol,aggregated)
        top3 = [('a',sumA)]
        self.assertEqual(top3,brandList.getTopAggregatedBrands(3))
        self.assertEqual(top3,brandList.getBottomAggregatedBrands(3))
        return
        
    
if __name__=='__main__':
    unittest.main()
    
