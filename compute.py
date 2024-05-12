import streamlit as st
import pandas as pd
from data import InvestData

def wealth_in_currency(data : InvestData, currency : str):
    # Join assets with stock prices and sum amount * price
    joined = data.assets.join(data.stocks, how='left')
    # For assets with no currency, set it to its own name
    joined['Currency'] = joined['Currency'].fillna(joined.index.to_series())
    joined['Price'] = joined['Price'].fillna(1)
    joined['Value'] = joined['Amount'] * joined['Price']
    # Sum all currencies held
    values = joined.groupby('Currency')['Value'].sum().to_frame()
   
    # Join with currency conversion, matching the currency index with the From column
    conversions = values.merge(data.currencies, left_on='Currency', right_on='From', how='inner')
    # Filter to only the currency we want to convert to. Note we ignore rows where the currency is the same as the target currency
    conversions = conversions[conversions['To'] == currency]
    conversions['Converted Value'] = conversions['Value'] * conversions['Price']
    
    final_amount = conversions['Converted Value'].sum() + values[values.index == currency]['Value'].sum()
    return final_amount
    