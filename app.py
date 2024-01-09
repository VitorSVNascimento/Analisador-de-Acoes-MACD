import streamlit as st
import pandas as pd
from constants import * 
import finance as fin
from plot import plot_action_graphic
import traceback
# from fbprophet import Prophet
# from fbprophet.plot import plot_plotly, plot_components_plotly

def get_action_list():
   return pd.read_csv('actions.csv') 

@st.cache_data
def get_finance_dataset(acronym,period='1m',data_interval='1d'):
   try:
      return fin.get_finance_dataset(acronym,period,data_interval)
   except Exception:
      traceback.print_exc()
      return ERROR_STRING

@st.cache_data
def insert_ema_and_macd_values(dataset):
   dataset[EMA_SHORT] = dataset[MAIN_COLUMN].ewm(span=SHORT_WINDOW,min_periods=SHORT_WINDOW).mean()
   dataset[EMA_LONG] = dataset[MAIN_COLUMN].ewm(span=LONG_WINDOW,min_periods=LONG_WINDOW).mean()
   dataset[MACD_VAL] = dataset[EMA_SHORT] - dataset[EMA_LONG]
   dataset[MACD_SIGNAL] = dataset[MACD_VAL].ewm(span=SIGNAL_WINDOW,min_periods=SIGNAL_WINDOW).mean()
   return dataset

def make_sliders(options_list,what_is_selected_name:str):
   selected_option_index = st.sidebar.slider(f'Selecione o {what_is_selected_name.lower()}:', 0, len(options_list) - 1, 0)
   selected_option = options_list[selected_option_index]
   st.sidebar.write(f'{what_is_selected_name.capitalize()} selecionado:', selected_option)
   return selected_option

st.title('Análise de ações')
st.sidebar.header('Escolha a ação')


df = get_action_list()

action = df[COMBINATION_COLUMN]
choose_action_name = st.sidebar.selectbox('Escolha uma ação:',action)

# Obtem o periodo selecionado
period_list = ['1d','1mo','2mo','3mo','4mo','5mo','6mo','7mo','8mo','9mo','10mo','11mo','1y']
selected_period = make_sliders(period_list,PERIOD_TEXT_NAME)

# Obtem o intervalo selecionado
interval_list = ['1m','5m','15m','30m','1h','1d','1mo']
selected_interval = make_sliders(interval_list,INTERVAL_TEXT_NAME)

#
max_profit_percentage = st.number_input("Insira a porcentagem mínima de lucro em cada venda", min_value=0.0, max_value=500.0, value=0.5000, step=0.0001) / 100
max_profit_percentage+=1

max_loss_percentage = st.number_input("Insira a porcentagem maxima de perda em cada venda", min_value=0.0, max_value=500.0, value=0.5000, step=0.0001) / 100
max_loss_percentage = 1 - max_loss_percentage
df_choose_action = df[df[COMBINATION_COLUMN] == choose_action_name]
acronym_choose_action = df_choose_action.iloc[0][ACRONYM_COLUMN]

df_history = get_finance_dataset(acronym_choose_action,selected_period,selected_interval)

if type(df_history) != str and not df_history.empty:
   df_history = insert_ema_and_macd_values(df_history)

   buy_index,sell_index = fin.get_buy_and_sell_index(df_history,max_profit_percentage,max_loss_percentage)

   st.subheader(f'Grafico da ação - {df_choose_action.iloc[0][NAME_COLUMN]}')

   st.plotly_chart(plot_action_graphic(df_history,buy_index,sell_index))
else:
   st.subheader(ERROR_STRING)
