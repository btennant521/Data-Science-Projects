import csv
import pandas as pd

def MSSDAC(A,low=0,high=None):
    if high==None: high = len(A)-1
    #base case
    if low == high:
        if A[low] > 0: return A[low], low, low
        else: return 0, low, low
    #divide
    mid = (low+high)//2
    #conquer
    maxLeft, buyLeft, sellLeft = MSSDAC(A, low, mid)
    maxRight, buyRight, sellRight  = MSSDAC(A, mid+1, high)

    #middle portion
    #find minimum buy price in lower half and maximum
    #buy price in upper half
    maxLeft2Center = left2Center = 0
    buyMid = low
    for i in range(mid, low-1,-1):
        left2Center += A[i]
        if left2Center > maxLeft2Center:
            maxLeft2Center = left2Center
            buyMid = i

    maxRight2Center = right2Center = 0
    sellMid = mid
    for i in range(mid+1, high+1):
        right2Center += A[i]
        if right2Center > maxRight2Center:
            maxRight2Center = right2Center
            sellMid = i

    maxMid = maxLeft2Center+maxRight2Center

    #
    if maxRight > maxLeft:
        if maxMid > maxRight:
            return round(maxMid,2), buyMid, sellMid
        else:
            return round(maxRight,2), buyRight, sellRight
    else:
        if maxMid > maxLeft:
            return round(maxMid,2), buyMid, sellMid
        else:
            return round(maxLeft,2), buyLeft, sellLeft

dat = pd.read_csv('prices-split-adjusted.csv')
securities = pd.read_csv('securities.csv')

tickers = {'AAPL','GOOGL'}
largestProfit = 0
winner = ''
winnerName = ''
bestSellidx = 0
bestBuyidx = 1
for tick in securities['Ticker symbol']:
    tickDat = dat[dat['symbol']==tick]
    dates = tickDat['date']
    if len(tickDat) >0:
        difs = [tickDat['close'].iloc[i+1]-tickDat['close'].iloc[i] for i in range(len(tickDat['close'])-1)]
        res = MSSDAC(difs)
    else:
        res=0,0,0
    if res[0] > largestProfit:
        winnerName = securities[securities['Ticker symbol']==tick]['Security'].to_string()[5:]
        largestProfit  = res[0]
        bestBuyidx = res[1]
        bestSellidx = res[2]
        bestBuyDate = dates.iloc[res[1]]
        bestSellDate = dates.iloc[res[2]]

print('Best stock to buy:',winnerName,' on:',bestBuyDate," and sell on:",bestSellDate,'with a profit of',largestProfit)
