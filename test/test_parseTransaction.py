'''
This file contains unittests for Finsbury Foods

@author : John Greenall
@date : 15-12-2013
'''
import sys
import os
from datetime import datetime
from datetime import tzinfo
import unittest
testFolder = os.path.split(os.path.realpath(__file__))[0]
baseFolder = os.path.split(testFolder)[0]
if not baseFolder in sys.path:sys.path.append(baseFolder)
import finsburyStructures as structs
import finsburyInput as finsIn

TEST_TRANSACTION_FILE = os.path.join(testFolder,'transactionSample.csv')
TEST_STOCK_FILE = os.path.join(testFolder,'stocklistSample.xml')
TEST_STOCK_FILE_EUR = os.path.join(testFolder,'stocklistSampleEuro.xml')
TEST_STOCK_FILE_CUR = os.path.join(testFolder,'stocklistSampleCur.xml')
TEST_STOCK_FILE_BAT = os.path.join(testFolder,'stocklistSampleBat.xml')


EAN1 = '0746817152012'        
EAN2 = '8014215020045'

class FinsburyInputTester(unittest.TestCase):
    def test_parseCsv(self):
        self.assertRaises(IOError,finsIn.parseTransactionCsv,'/pathToNon-Existent.file')
        
        transDict = finsIn.parseTransactionCsv(TEST_TRANSACTION_FILE)
        self.assertDictEqual(transDict,{EAN1: 1, EAN2: 8})
        
    def test_fromDate(self):
        #now check date constraints work: first just startDate
        fromD = datetime(day=25,month=10,year=2011,hour=13,minute=43)
        self.assertDictEqual(finsIn.parseTransactionCsv(TEST_TRANSACTION_FILE,fromDate=fromD),{EAN2:8})
    
    def test_fromToDate(self):
        #now endDate
        fromD = datetime(day=25,month=10,year=2011,hour=13,minute=42)
        toD = datetime(day=25,month=10,year=2011,hour=13,minute=43)
        self.assertDictEqual(finsIn.parseTransactionCsv(TEST_TRANSACTION_FILE,fromDate=fromD,toDate=toD),{EAN1:-3})
        
    def test_parseStockErrorOnCurrencyType(self):
        #non-GBP currency
        self.assertRaises(finsIn.InvalidCurrency,finsIn.parseWestBun,TEST_STOCK_FILE_EUR)
        return

    def test_parseStockErrorOnCurrency(self):
        #currency value not parsable
        self.assertRaises(finsIn.InvalidCurrency,finsIn.parseWestBun,TEST_STOCK_FILE_CUR)
        return
    
    def test_parseStockErrorOnBatchsize(self):
        #currency batchSize not parsable
        self.assertRaises(ValueError,finsIn.parseWestBun,TEST_STOCK_FILE_BAT)
        return       
    
    def test_parseStocklistOnly(self):
        
        
        res = {EAN1:structs.StockInfo(ean=EAN1,batchsize=24,brand='V05',quantity='150ml',margin=269,sellthroughPr=699,
                                      name='hair gel - extra strong',nSold=0,profit=0,wholesalePr=430),
               EAN2:structs.StockInfo(ean=EAN2,batchsize=20,brand='Alisea',quantity='50cl',margin=70,sellthroughPr=210,
                                                     name='Naturale Italian mineral water',nSold=0,profit=0,wholesalePr=140)               }
        self.assertDictEqual(res,finsIn.parseWestBun(TEST_STOCK_FILE))
        
    def test_parseStockAndTransactions(self):
        EAN1 = '0746817152012'        
        EAN2 = '8014215020045'
        transDict = finsIn.parseTransactionCsv(TEST_TRANSACTION_FILE)
        
        res = {EAN1:structs.StockInfo(ean=EAN1,batchsize=24,brand='V05',quantity='150ml',margin=269,sellthroughPr=699,
                                      name='hair gel - extra strong',nSold=transDict[EAN1],profit=269*transDict[EAN1],wholesalePr=430),
               EAN2:structs.StockInfo(ean=EAN2,batchsize=20,brand='Alisea',quantity='50cl',margin=70,sellthroughPr=210,
                                                     name='Naturale Italian mineral water',nSold=transDict[EAN2],profit=70*transDict[EAN2],
                                                     wholesalePr=140)               }
        self.assertDictEqual(res,finsIn.parseWestBun(TEST_STOCK_FILE,transDict))        
        return
        
        
    
if __name__=='__main__':
    unittest.main()
    