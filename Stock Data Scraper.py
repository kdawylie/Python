import pandas as pd
from bs4 import BeautifulSoup
import requests

def price_extraction(ticker):
    r = requests.get(f'https://www.marketwatch.com/investing/stock/{ticker}')
    soup = BeautifulSoup(r.text, 'html.parser')
    raw_metrics = soup.find_all('h2', {'class':'intraday__price'})
    clean_metrics = {'ticker':ticker}
    for individual_metric in raw_metrics:
        label = "Current Price"
        primary = individual_metric.find('bg-quote', {'class':'value'}).text
        clean_metrics[label] = primary
    return clean_metrics

def stats_extraction(ticker):
    r = requests.get(f'https://www.marketwatch.com/investing/stock/{ticker}')
    soup = BeautifulSoup(r.text, 'html.parser')
    raw_metrics = soup.find_all('li', {'class':'kv__item'})
    clean_metrics = {'ticker': ticker}
    for individual_metric in raw_metrics:
        label = individual_metric.find('small', {'class':'label'}).text
        primary = individual_metric.find('span', {'class':'primary'}).text
        clean_metrics[label] = primary        
    return clean_metrics

def get_stats_df(stock):
    stock_list = []
    stock_list.append(stats_extraction(stock))
        
    final_df1 = pd.DataFrame(stock_list)
    return final_df1

def get_price_df(stock):
    stock_list = []
    stock_list.append(price_extraction(stock))

    final_df2 = pd.DataFrame(stock_list)
    return final_df2

ticker = input('Which ticker would you like to look up?\n')

stock_df1 = get_price_df(ticker)
stock_df2 = get_stats_df(ticker)

stock_df = pd.merge(stock_df1,stock_df2, how='inner',on='ticker')

print('\n\nHere is your stock data!')
print(f'\n\n{stock_df}')