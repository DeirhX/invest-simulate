import streamlit as st
import compute
import data
from menu import menu
from data import get_investments
from ux import show_assets_dataframe

st.set_page_config(page_title='Nákup akcií', layout='centered')
st.subheader('Nákup / prodej akcií')
menu() 

investments = get_investments()
show_assets_dataframe(compute.assets_with_prices(investments))

with st.container():
    st.write('Nákup')
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        asset = st.selectbox('Akcie', investments.get_asset_names())
    with col2:
        amount = st.number_input('Množství', min_value=0, value=1)
    cost = amount * investments.stocks.loc[asset, "Price"]
    currency = investments.stocks.loc[asset, "Currency"]
    st.markdown(f'Nákup: :green[{amount:.2f} {asset}] za :red[{cost:.2f} {currency}] při kurzu :blue[{investments.stocks.loc[asset, "Price"]:.2f} {currency}] za kus')
    if investments.get_assets().loc[currency, 'Amount'] < cost:
        st.error('Nemáte dostatek peněz na nákup')
    else: 
        if st.button('Potvrdit nákup'):
            data = compute.buy(data, asset, amount, currency)
            st.success('Nákup proběhl úspěšně')
            show_assets_dataframe(compute.assets_with_prices(data))