'''
This file contains the functionality for parsing the transaction files from Finsbury Foods

@author : John Greenall
@date : 15-12-2013
'''
import csv
import os
import finsburyStructures as structs
from collections import defaultdict
from xml.dom import minidom
from dateutil import parser
import stdnum.ean

class InvalidCurrency(Exception):
    '''
    exception used to indicate incorrect currency type in input
    '''

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


def parseWestBun(fname,transactionDict=defaultdict(int),warn=False):
    '''
    @param[in] fname string, path to input file
    @param[in] transactionDict defaultdict with ean as key, nSold as val
    
    @return stockDict dictionary with ean as key, StockInfo object as val
    '''
    if not os.path.exists(fname):
        raise IOError('Cannot find input file. Please check path : {}'.format(fname))    
    stock = dict()
    with open(fname,'r') as infile:
        xml = minidom.parse(infile)
        stocklist = xml.childNodes[0]
        for s in stocklist.getElementsByTagName('line'):
            #first check ean valid
            try:
                ean = stdnum.ean.validate(s.getAttribute('ean'))
                thisObj = {'ean':ean}
            except Exception, e:
                if warn:
                    print('warning : invalid ean number {} ignored'.format(ean))
                continue
            thisObj['nSold'] = transactionDict[ean]
 
                
            #these feilds just map 1-1 with the attributes in StockInfo and can be treated the same
            stdFields = ['name','brand','quantity','batchsize']
            types = [str,str,str,int]
            for f,t in zip(stdFields,types):
                n = s.getElementsByTagName(f)[0]
                try:
                    thisObj[f] = t(n.childNodes[0].data)
                except ValueError,e:
                    raise ValueError('Invalid value for {} of product with ean: {}. Should be of type: {}'.format(f,ean,type))
                
            
            #now handle prices slightly differently
            for price in s.getElementsByTagName('price'):
                if not price.getAttribute('currency') == 'GBP':
                    raise InvalidCurrency('all currencies must be in GBP')
                try:
                    pence = int(price.childNodes[0].data.replace('.',''))
                except ValueError:
                    raise InvalidCurrency('Invalid currency value for product with ean: {}'.format(ean))
                priceType = price.getAttribute('type')
                thisObj[structs.StockInfo.priceFieldname[priceType]] = pence
            
            thisObj['margin'] = thisObj['sellthroughPr'] - thisObj['wholesalePr']
            thisObj['profit'] = thisObj['margin']*thisObj['nSold']
            stock[ean] = structs.StockInfo(**thisObj)
                     
    
    return stock

