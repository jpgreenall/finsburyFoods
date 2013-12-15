import sys
import os
from datetime import datetime
from datetime import tzinfo
import unittest
sys.path.append(os.path.split(os.getcwd())[0])
import finsburyStructures as structs
import finsburyInput as finsIn

TEST_FILE = os.path.join(os.getcwd(),'transactionSample.csv')
class FinsburyInputTester(unittest.TestCase):
    def test_parseCsv(self):
        self.assertRaises(IOError,finsIn.parseTransactionCsv,'/pathToNon-Existent.file')
        
        transDict = finsIn.parseTransactionCsv(TEST_FILE)
        self.assertDictEqual(transDict,{'0746817152012': 1, '8014215020045': 8})
        #now check date constraints work: first just startDate
        fromD = datetime(day=25,month=10,year=2011,hour=13,minute=43)
        self.assertDictEqual(finsIn.parseTransactionCsv(TEST_FILE,fromDate=fromD),{ '8014215020045': 8}) 
        #now endDate
        fromD = datetime(day=25,month=10,year=2011,hour=13,minute=42)
        toD = datetime(day=25,month=10,year=2011,hour=13,minute=43)
        self.assertDictEqual(finsIn.parseTransactionCsv(TEST_FILE,fromDate=fromD,toDate=toD),{ '0746817152012':-3}) 
        return
    
if __name__=='__main__':
    unittest.main()
    