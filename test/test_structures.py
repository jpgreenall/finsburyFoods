import sys
import os
sys.path.append(os.path.split(os.getcwd())[0])
import finsburyStructures as structs
import unittest


class FinsburyStructTester(unittest.TestCase):
    def test_init(self):
        #make sure slots have been correctly set up to raise when non existent field used
        self.assertRaises(AttributeError,structs.StockInfo,nonExistentField=1)
        return
    
if __name__=='__main__':
    unittest.main()
    