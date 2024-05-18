import math
import streamlit as st
from menu import menu
from data import get_investments
import ux

st.set_page_config(page_title='Kurzy měn', layout='centered')
st.subheader('Správa měn')
menu() 

investments = st.session_state.get('data', None) or get_investments()
st.session_state.data = investments

currencies = investments.get_currency_names()

st.markdown('Aktuální majetek')
# Get view on assets that are currencies
def compute_currency_assets(investments):
    return investments.get_assets().loc[investments.get_assets().index.isin(currencies)]

currency_assets = compute_currency_assets(investments)
currency_view = ux.show_funds_dataframe(currency_assets, width=350)
st.divider()

with st.container():
    caption = st.markdown('')
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2.3])
    with col1:
        source = st.selectbox('Zkonvertovat', investments.get_currency_names())
    with col2:
        target = st.selectbox('Na měnu', investments.get_exchangable_currencies(source))
    with col3:
        target_amount = st.number_input(f'Množství {target}', value=0.0, min_value=0.0, key='amount', step=1.0, format="%.2f")
        
    if source is None or target is None:
        caption.markdown('Vyberte z které měny na kterou konvertovat')
    if target_amount == 0:
        caption.markdown(f'Vyberte kolik :blue[{source}] chcete zkonvertovat na :red[{target}].')
    elif target_amount > 0:
        rate = investments.get_exchange_rate(source, target)
        cost = target_amount * rate
        source_amount = cost
        caption.markdown('Nákup')
        st.markdown(f'Výměna :green[{source_amount:.2f} {source}] na :red[{target_amount:.2f} {target}] při kurzu :blue[{rate:.2f} {source}] za kus')
        if source not in investments.get_assets().index:
            st.error('Nemáte dostatek peněz na nákup')
        elif cost > investments.get_assets().loc[source, 'Amount']:
            st.error(f'Nemáte dostatek peněz na nákup, maximum lze nakoupit :green[{math.ceil(investments.get_assets().loc[source, "Amount"]/rate * 100 - 1) / 100:.2f} {target}]')
        else: 
            if st.button('Potvrdit konverzi měn'):
                with st.spinner(f'Probíhá konverze :green[{source}] na :red[{target}]...'):
                    data = investments.buy(target, target_amount, source)
                    investments.save()
                    st.cache_data.clear()
                    st.success('Nákup proběhl úspěšně')
                    currency_assets = compute_currency_assets(investments)
                    currency_view.dataframe(currency_assets, width=350, column_order=ux.get_show_funds_config()['column_order'], column_config=ux.get_show_funds_config()['column_config'])

with st.container():
    st.markdown('Aktuální kurzy měn')
    st.dataframe(investments.currencies.sort_values(by='From'), hide_index=True, width=350,
                column_order=['From', 'Price', 'To'], 
                column_config={'From': st.column_config.TextColumn("Za"),
                                'To': st.column_config.TextColumn("Čeho"),
                                'Price': st.column_config.NumberColumn("Dostanu", format="%.3f")})