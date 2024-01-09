from constants import *
import plotly.graph_objects as go
import plotly as pio
from plotly.subplots import make_subplots


def plot_action_graphic(dataset,buy_index,sell_index):
    max_tick = max(max(dataset[MACD_VAL]),max(dataset[MACD_SIGNAL]))
    min_tick = min(min(dataset[MACD_VAL]),min(dataset[MACD_SIGNAL]))    
    fig = make_subplots(vertical_spacing=0, rows=2, cols=1, row_heights=[5, 4])
    fig.add_trace(go.Scatter(x=dataset.index, y=dataset[MAIN_COLUMN], name=f"{MAIN_COLUMN} price", line=dict(color='green')))
    fig.add_trace(go.Scatter(x=dataset.index, y=dataset[MACD_VAL], name=f"{MACD_VAL}", line=dict(color='blue')), row=2, col=1)
    fig.add_trace(go.Scatter(x=dataset.index, y=dataset[MACD_SIGNAL], name=f"{MACD_SIGNAL}", line=dict(color='orange')), row=2, col=1)

    fig.add_trace(go.Scatter(x=dataset.index[buy_index], y=dataset[MAIN_COLUMN][buy_index],
                            mode='markers', marker=dict(size=8, color='blue', symbol='circle'),
                            name='Buy Signal'), row=1, col=1)
    fig.add_trace(go.Scatter(x=dataset.index[sell_index], y=dataset[MAIN_COLUMN][sell_index],
                            mode='markers', marker=dict(size=8, color='red', symbol='circle'),
                            name='Sell Signal'), row=1, col=1)

    fig.update_layout(xaxis_rangeslider_visible=False,
                    xaxis=dict(zerolinecolor='black', showticklabels=False),
                    xaxis2=dict(showticklabels=False))
    fig['layout']['yaxis2'].update(range=[min_tick, max_tick])

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=False)
    return fig
