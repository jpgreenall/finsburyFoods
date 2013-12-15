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

class FinsburyInputTester(unittest.TestCase):
    def test_parseCsv(self):
        self.assertRaises(IOError,finsIn.parseTransactionCsv,'/pathToNon-Existent.file')
        
        transDict = finsIn.parseTransactionCsv(TEST_TRANSACTION_FILE)
        self.assertDictEqual(transDict,{'0746817152012': 1, '8014215020045': 8})
        
    def test_fromDate(self):
        #now check date constraints work: first just startDate
        fromD = datetime(day=25,month=10,year=2011,hour=13,minute=43)
        self.assertDictEqual(finsIn.parseTransactionCsv(TEST_TRANSACTION_FILE,fromDate=fromD),{ '8014215020045': 8})
    
    def test_fromToDate(self):
        #now endDate
        fromD = datetime(day=25,month=10,year=2011,hour=13,minute=42)
        toD = datetime(day=25,month=10,year=2011,hour=13,minute=43)
        self.assertDictEqual(finsIn.parseTransactionCsv(TEST_TRANSACTION_FILE,fromDate=fromD,toDate=toD),{ '0746817152012':-3})
    
    def test_parseStocklistOnly(self):
        result = finsIn.parseWestBun(TEST_STOCK_FILE)
        EAN1 = '0746817152012'        
        EAN2 = '8014215020045'
        
        res = {EAN1:structs.StockInfo(ean=EAN1,batchsize=24,brand='V05',quantity='150ml',margin=269,sellthroughPr=699,
                                      name='hair gel - extra strong',nSold=0,profit=0,wholesalePr=430),
               EAN2:structs.StockInfo(ean=EAN2,batchsize=20,brand='Alisea',quantity='50cl',margin=70,sellthroughPr=210,
                                                     name='Naturale Italian mineral water',nSold=0,profit=0,wholesalePr=140)               }
        self.assertDictEqual(res,finsIn.parseWestBun(TEST_STOCK_FILE))
        
    def test_parseStockAndTransactions(self):
        return
        
        
    
if __name__=='__main__':
    unittest.main()
    