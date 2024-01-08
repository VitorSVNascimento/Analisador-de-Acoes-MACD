import streamlit as st
import pandas as pd
from datetime import date
from constants import * 
import finance as fin
from plot import plot_action_graphic
# from fbprophet import Prophet
# from fbprophet.plot import plot_plotly, plot_components_plotly
# from plotly import graph_objs as go

# PERIOD = '1y'

st.title('Análise de ações')
st.sidebar.header('Escolha a ação')

def get_action_list():
   return pd.read_csv('actions.csv') 

df = get_action_list()

action = df[COMBINATION_COLUMN]
choose_action_name = st.sidebar.selectbox('Escolha uma ação:',action)

period_list = ['1d','1mo','2mo','3mo','4mo','5mo','6mo','7mo','8mo','9mo','10mo','11mo','1y']
selected_period_index = st.sidebar.slider('Selecione o período:', 0, len(period_list) - 1, 0)

# Use o índice selecionado para obter o valor correspondente da lista
selected_period = period_list[selected_period_index]

# Exiba o período selecionado
st.sidebar.write('Período selecionado:', selected_period)

interval_list = ['1m','5m','15m','30m','1h','1d','1mo']
selected_interval_index = st.sidebar.slider('Selecione o período:', 0, len(interval_list) - 1, 0)

# Use o índice selecionado para obter o valor correspondente da lista
selected_interval = interval_list[selected_interval_index]

# Exiba o período selecionado
st.sidebar.write('Intervalo selecionado:', selected_interval)


df_choose_action = df[df[COMBINATION_COLUMN] == choose_action_name]

acronym_choose_action = df_choose_action.iloc[0][ACRONYM_COLUMN]

print(f'Ação selecionada == {acronym_choose_action}')

df_history = fin.get_finance_dataset(acronym_choose_action,selected_period,selected_interval)

df_history[EMA_SHORT] = df_history[MAIN_COLUMN].ewm(span=SHORT_WINDOW,min_periods=SHORT_WINDOW).mean()
df_history[EMA_LONG] = df_history[MAIN_COLUMN].ewm(span=LONG_WINDOW,min_periods=LONG_WINDOW).mean()
df_history[MACD_VAL] = df_history[EMA_SHORT] - df_history[EMA_LONG]
df_history[MACD_SIGNAL] = df_history[MACD_VAL].ewm(span=SIGNAL_WINDOW,min_periods=SIGNAL_WINDOW).mean()

buy_index,sell_index = fin.get_buy_and_sell_index(df_history)

st.subheader(f'Grafico da ação - {df_choose_action.iloc[0][NAME_COLUMN]}')

st.plotly_chart(plot_action_graphic(df_history,buy_index,sell_index))
