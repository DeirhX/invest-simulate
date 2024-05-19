import streamlit as st
import compute
import auth
import ux
from menu import menu
from data import get_investments

st.set_page_config(page_title='Nákup akcií', layout='centered')
st.subheader('Nákup / prodej akcií')
menu() 
auth.need_login()

investments = st.session_state.get('data', None) or get_investments()
st.session_state.data = investments

asset_view = ux.show_assets_dataframe(compute.assets_with_prices(investments))

with st.container():
    caption = st.markdown('')
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        asset = st.selectbox('Akcie', investments.get_asset_names())
    with col2:
        amount = st.number_input('Množství', value=1.0, key='amount', step=1.0, format="%.2f")
    cost = amount * investments.stocks.loc[asset, "Price"]
    currency = investments.stocks.loc[asset, "Currency"]
    if amount == 0:
        caption.markdown('Vyberte :blue[počet] akcií k nákupu :green[(kladný)] / prodeji :red[(záporný)].')
    elif amount > 0:
        caption.markdown('Nákup')
        st.markdown(f'Nákup: :green[{amount:.2f} {asset}] za :red[{cost:.2f} {currency}] při kurzu :blue[{investments.stocks.loc[asset, "Price"]:.2f} {currency}] za kus')
        if currency not in investments.get_assets().index:
            st.error('Nemáte dostatek peněz na nákup')
        elif cost > investments.get_assets().loc[currency, 'Amount']:
            st.error(f'Nemáte dostatek peněz na nákup, maximum lze nakoupit :green[{investments.get_assets().loc[currency, "Amount"]/investments.stocks.loc[asset, "Price"]:.2f} {asset}]')
        else: 
            if st.button('Potvrdit nákup'):
                with st.spinner('Probíhá nákup...'):
                    data = investments.buy(asset, amount, currency)
                    investments.save()
                    st.cache_data.clear()
                    st.success('Nákup proběhl úspěšně')
                    asset_view.dataframe(compute.assets_with_prices(investments), column_order=ux.get_show_assets_config()['column_order'], column_config=ux.get_show_assets_config()['column_config'])
    else: # amount < 0
        caption.markdown('Prodej')
        st.markdown(f'Prodej: :red[{-amount:.2f} {asset}] za :green[{-cost:.2f} {currency}] při kurzu :blue[{investments.stocks.loc[asset, "Price"]:.2f} {currency}] za kus')
        if asset not in investments.get_assets().index:
            st.error('Nemáte dostatek akcií k prodeji')
        elif investments.get_assets().loc[asset, 'Amount'] < -amount:
            st.error(f'Nemáte dostatek akcií k prodeji, maximum je :red[{investments.get_assets().loc[asset, "Amount"]:.2f} {asset}]')
        else: 
            if st.button('Potvrdit prodej'):
                with st.spinner('Probíhá prodej...'):
                    data = investments.buy(asset, amount, currency)
                    investments.save()
                    st.cache_data.clear()
                    st.success('Prodej proběhl úspěšně')
                    asset_view.dataframe(compute.assets_with_prices(investments), column_order=ux.get_show_assets_config()['column_order'], column_config=ux.get_show_assets_config()['column_config'])

st.session_state.data = investments            
            
# Make some space
st.write('')
st.caption('Historie obchodů')
ux.show_trades_dataframe(investments.get_trades())