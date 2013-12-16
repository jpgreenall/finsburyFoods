#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This file contains the main summary function for Finsbury Foods

@author : John Greenall
@date : 15-12-2013
'''
import sys

import finsburyStructures as structs
import finsburyInput as finsIn


def formatCash(pence):
    '''
    @param[in] pence integer value of cash in pence
    @return cash value as string in format £pp.pp
    '''
    if pence < 0:
        return '-{}'.format(formatCash(-pence))
    else:
        pounds = pence/100
        return '£{:,d}.{}'.format(pounds,pence-(pounds*100))

def summarizeTransactions(stockfile,transfile):
    '''
    Print the summary of transactions in the specified files.
    For file format specification see appropriate classes in finsburyInput
    @param[in] stockfile filename to be parsed by parseWestBun
    @param[in] transfile filename to be parsed by parseTransactionsCsv
    '''
    transDict = finsIn.parseTransactionCsv(transfile)
    summary = finsIn.parseWestBun(stockfile,transactionDict=transDict)
    
    summaryList = structs.StockInfoList(summary.values())
    
    print('Total profit:')
    print(formatCash(summaryList.getTotalProfit()))

    print('\nTop 3 products by profit:')
    top = summaryList.getTopNProfits(3)
    for i,s in enumerate(top):
        print('{}. {:<40} {:>12}'.format(i,s.name,formatCash(s.profit)))
    print('\nBottom 3 products by profit:')
    bot = summaryList.getBottomNProfits(3)
    for i,s in enumerate(bot):
        print('{}. {:<40} {:>12}'.format(i,s.name,formatCash(s.profit)))

    print('\nTop 3 products by quantity:')
    top = summaryList.getTopNQuantities(3)
    for i,s in enumerate(top):
        print('{}. {:<40} {:>12,d}'.format(i,s.name,s.nSold))
    print('\nBottom 3 products by quantity:')
    bot = summaryList.getBottomNQuantities(3)
    for i,s in enumerate(bot):
        print('{}. {:<40} {:>12,d}'.format(i,s.name,s.nSold))
    
    #Display the top 3 brands by quantity sold.
    print('\nTop 3 brands by quantity sold:')
    topB = summaryList.getTopAggregatedBrands(3)
    for i,s in enumerate(topB):
        print('{}. {:<40} {:>12,d}'.format(i,s[0],s[1]))
        
    print('\nBottom 3 brands by quantity sold:')
    bottomB = summaryList.getBottomAggregatedBrands(3)
    for i,s in enumerate(bottomB):
        print('{}. {:<40} {:>12,d}'.format(i,s[0],s[1]))    
    
    
    return


if __name__=='__main__':
    if not len(sys.argv) == 3:
        raise ValueError('usage : python finsburySummary.py <stockfile> <transactionfile>')
    summarizeTransactions(stockfile=sys.argv[1],transfile=sys.argv[2])