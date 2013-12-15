'''
This file contains the functionality for parsing the transaction files from Finsbury Foods

@author : John Greenall
@date : 15-12-2013
'''
import csv
import os
import finsburyStructures as structs
from collections import defaultdict
from dateutil import parser
import stdnum.ean

def parseTransactionCsv(fname,fromDate=None,toDate=None,warn=False):
    '''
    @param[in] fname string, path to input file
    
    @return nSold - dictionary with ean as key, transaction count as value
    '''
    if not os.path.exists(fname):
        raise IOError('Cannot find input file. Please check path : {}'.format(fname))
    transCount = defaultdict(int)
    with open(fname,'r') as infile:
        while(True):
            try:
                transDate,transId,ean,n = infile.readline().split(',')
            except ValueError: # hit end of file
                break            
            #first check ean valid
            try:
                ean = stdnum.ean.validate(ean)
            except Exception, e:
                if warn:
                    print('warning : invalid ean number {} ignored'.format(ean))
                continue
            #now check date falls between dates supplied
            d = parser.parse(transDate,ignoretz=True)
            if (fromDate is None or d >= fromDate) and (toDate is None or d < toDate):
                transCount[ean] += int(n)
            
    
    return transCount
