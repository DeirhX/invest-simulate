import streamlit as st
import pandas as pd

def show_assets_dataframe(assets: pd.DataFrame):
    st.dataframe(assets, hide_index=False,
             column_order=['Asset', 'Amount', 'Price', 'Currency', 'Value'], 
             column_config={'Asset': st.column_config.TextColumn("Instrument"),
                            'Amount': st.column_config.NumberColumn("Množství", format="%.2f"),
                            'Price': st.column_config.NumberColumn("Aktuální cena", format="%.2f"),
                            'Currency': st.column_config.TextColumn("Měna"),
                            'Value': st.column_config.NumberColumn("Hodnota", format="%.2f")})