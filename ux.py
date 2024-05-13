import streamlit as st
import pandas as pd

def get_show_assets_config():
    return {'column_order': ['Asset', 'Amount', 'Price', 'Currency', 'Value'],
            'column_config': {'Asset': st.column_config.TextColumn("Instrument"),
                              'Amount': st.column_config.NumberColumn("Množství", format="%.2f"),
                              'Price': st.column_config.NumberColumn("Aktuální cena", format="%.2f"),
                              'Currency': st.column_config.TextColumn("Měna"),
                              'Value': st.column_config.NumberColumn("Hodnota", format="%.2f")}
            }

def show_assets_dataframe(assets: pd.DataFrame):
    return st.dataframe(assets, hide_index=False,
             column_order=['Asset', 'Amount', 'Price', 'Currency', 'Value'], 
             column_config={'Asset': st.column_config.TextColumn("Instrument"),
                            'Amount': st.column_config.NumberColumn("Množství", format="%.2f"),
                            'Price': st.column_config.NumberColumn("Aktuální cena", format="%.2f"),
                            'Currency': st.column_config.TextColumn("Měna"),
                            'Value': st.column_config.NumberColumn("Hodnota", format="%.2f")})
    
def show_trades_dataframe(trades: pd.DataFrame):
    return st.dataframe(trades.sort_values(by='Time', ascending=False), hide_index=True, 
             column_order=['Time', 'Asset', 'Amount', 'Currency', 'Price', 'Proceeds'], 
             column_config={
                    'Time': st.column_config.DatetimeColumn("Čas"),
                    'Asset': st.column_config.TextColumn("Instrument"),
                    'Amount': st.column_config.NumberColumn("Množství", format="%.2f"),
                    'Currency': st.column_config.TextColumn("Měna"),
                    'Proceeds': st.column_config.NumberColumn("Celková cena", format="%.2f"),
                    'Price': st.column_config.NumberColumn("Cena za kus", format="%.2f"),
                    })