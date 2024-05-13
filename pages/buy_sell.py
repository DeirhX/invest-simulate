import streamlit as st
import compute
import data
from menu import menu
from data import get_investments
import ux
st.set_page_config(page_title='Nákup akcií', layout='centered')
st.subheader('Nákup / prodej akcií')
menu() 

investments = get_investments()
asset_view = ux.show_assets_dataframe(compute.assets_with_prices(investments))

with st.container():
    caption = st.markdown('')
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        asset = st.selectbox('Akcie', investments.get_asset_names())
    with col2:
        amount = st.number_input('Množství', value=1)
    cost = amount * investments.stocks.loc[asset, "Price"]
    currency = investments.stocks.loc[asset, "Currency"]
    if amount == 0:
        caption.markdown('Vyberte :blue[počet] akcií k nákupu :green[(kladný)] / prodeji :red[(záporný)].')
    elif amount > 0:
        caption.markdown('Nákup')
        st.markdown(f'Nákup: :green[{amount:.2f} {asset}] za :red[{cost:.2f} {currency}] při kurzu :blue[{investments.stocks.loc[asset, "Price"]:.2f} {currency}] za kus')
        if currency not in investments.get_assets().index or investments.get_assets().loc[currency, 'Amount'] < cost:
            st.error('Nemáte dostatek peněz na nákup')
        else: 
            if st.button('Potvrdit nákup'):
                with st.spinner('Probíhá nákup...'):
                    data = investments.buy(asset, amount, currency)
                    investments.save()
                    st.success('Nákup proběhl úspěšně')
                    asset_view.dataframe(compute.assets_with_prices(investments), column_order=ux.get_show_assets_config()['column_order'], column_config=ux.get_show_assets_config()['column_config'])
    else: # amount < 0
        caption.markdown('Prodej')
        st.markdown(f'Prodej: :red[{-amount:.2f} {asset}] za :green[{-cost:.2f} {currency}] při kurzu :blue[{investments.stocks.loc[asset, "Price"]:.2f} {currency}] za kus')
        if asset not in investments.get_assets().index or investments.get_assets().loc[asset, 'Amount'] < -amount:
            st.error('Nemáte dostatek akcií k prodeji')
        else: 
            if st.button('Potvrdit prodej'):
                with st.spinner('Probíhá prodej...'):
                    data = investments.buy(asset, amount, currency)
                    st.progress(0.2)
                    investments.save()
                    st.progress(1.0)
                    st.success('Prodej proběhl úspěšně')
                    asset_view.dataframe(compute.assets_with_prices(investments), column_order=ux.get_show_assets_config()['column_order'], column_config=ux.get_show_assets_config()['column_config'])
            
            
# Make some space
st.write('')
st.caption('Historie obchodů')
ux.show_trades_dataframe(investments.trades)