Title: Max Stock Profit
Author: Ben Tennant

This is a python program that takes in times series stock price data
and determines when the best time to purchase a particular
companies stock and how much profit one would have made.
This implementation uses a divide and conquer technique.
It uses the difference between prices at the close of 
each day to determine the max profit. The securities.csv
is used to bring in the list of unique tickers.

Attributes:

date: month/day/year

symbol: company stock ticker

open: price at opening of market

close: price at closing of market

low: lowest price of the day

high: highest price of the day

volume: volume of stock traded