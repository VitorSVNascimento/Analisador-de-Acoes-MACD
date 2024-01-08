import yfinance as yf
from constants import *
import numpy as np
def get_finance_dataset(acronym,period='1m',data_interval='1d'):
  df = yf.Ticker(acronym)
  df_history = df.history(period=period,interval=data_interval)
  return df_history

BUY = 1
SELL = 2
HOLD = 0

MAX_PROFIT_PERCENT = 1.10 #Valor mínimo de lucro em porcentagem
MAX_LOSS_PERCENT = 0.97 #Valor máximo de prejuizo em porcentagem
def decide_action(macd_val, signal_val, position, current_price, last_buy_price=0):
    if np.isnan(macd_val) or np.isnan(signal_val):
        return HOLD

    if macd_val > signal_val and position != BUY and abs(abs(macd_val) - abs(signal_val)) > 0.0013:
        return BUY

    elif macd_val < signal_val and position == BUY:
        potential_profit = current_price / last_buy_price
        return SELL if potential_profit >= MAX_PROFIT_PERCENT or potential_profit <= MAX_LOSS_PERCENT else HOLD
    else:
        return HOLD
    
def calc_roi(total_profit, initial_investment):
    roi = (total_profit / initial_investment) if initial_investment != 0 else 0
    return roi * 100

actions_json = {BUY:'buy',
                SELL:'sell',
                HOLD:'hold'}


def get_buy_and_sell_index(dataset):
    initial_investment = 1000
    available_cash = initial_investment
    last_buy_price = 0
    total_invested = 0
    total_profit = 0
    position = None
    buy_index = []
    sell_index = []

    for i in range(len(dataset)):
        action = decide_action(
            dataset[MACD_VAL][i],
            dataset[MACD_SIGNAL][i],
            position,
            dataset[MAIN_COLUMN][i],
            last_buy_price
        )
        if action == BUY:
            position = BUY
            buy_index.append(i)
            last_buy_price = dataset[MAIN_COLUMN][i]
            shares_bought = available_cash // last_buy_price
            total_cost = shares_bought * last_buy_price
            available_cash -= total_cost
            total_invested += total_cost

        elif action == SELL and position == BUY:
            position = SELL
            sell_index.append(i)
            sell_price = dataset[MAIN_COLUMN][i]
            available_cash += sell_price * shares_bought
            total_profit += (sell_price - last_buy_price) * shares_bought
        if action != HOLD:
            print(f"Data:{dataset.index[i]}\tValor: {dataset[MAIN_COLUMN][i]:.2f} \tAção: {actions_json[action]}")
    return buy_index,sell_index