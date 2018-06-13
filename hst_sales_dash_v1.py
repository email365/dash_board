import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime
import os
import dash_auth

###############################
# preparation
###############################

file_path = 'C:/Users/Administrator/Desktop/db2/'

second = 1000
minute = 60
hour   = 60
day    = 24
interval = 1/12*minute*second

###############################
# dash board
###############################

app = dash.Dash('auth')
auth = dash_auth.BasicAuth(
    app,
    (('total', 'hstmeeting2018',),)
)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

app.layout = html.Div(
    html.Div([
        dcc.Graph(id='live-update-graph-scatter', animate=True),
        dcc.Graph(id='live-update-graph-bar'),
        dcc.Graph(id='live-update-table'),
        dcc.Interval(
            id='interval-component',
            interval=interval
        )
    ])
)

#line
@app.callback(Output('live-update-graph-scatter', 'figure'),
              events=[Event('interval-component', 'interval')])
def update_graph_scatter():
    df1 = pd.read_csv(file_path+'df_ytd_week.csv',encoding='gbk')

    trace = [
        go.Trace(
            x=df1['week'],  # assign x as the dataframe column 'x'
            y=df1['净现金业绩'],
            name='净现金业绩'
        ),
        go.Trace(
            x=df1['week'],  # assign x as the dataframe column 'x'
            y=df1['本期收款'],
            name='本期收款'
        )
    ]

    layout = go.Layout(
        title='各周收款、净现金业绩',
        xaxis=dict(title='横坐标：周数'),
        yaxis=dict(title='金额(百万)')
    )
    return {'data': trace, 'layout':layout}

#bar chart
@app.callback(Output('live-update-graph-bar', 'figure'),
              events=[Event('interval-component', 'interval')])
def update_graph_bar():
    df2 = pd.read_csv(file_path+'total.csv',encoding='gbk')
    df2['月度完成率(%)'] = df2['月度完成率(%)'].astype(float)
    df2 = df2.sort_values(by=['年度达成率(%)','月度完成率(%)'])

    trace1 = go.Bar(
            x=df2.所属部门,
            y=df2['月度完成率(%)'],
            name = '月度完成率'
        )
    trace2 = go.Bar(
            x=df2.所属部门,
            y=df2['年度达成率(%)'],
            name = '年度达成率',
        )

    data = [trace1,trace2]

    # layout = plotly.graph_objs.Layout(
    layout = go.Layout(
        title='月度完成率、年度达成率',
        yaxis=dict(
            title='比率'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
        )

    return {'data': data, 'layout': layout}

# #table
@app.callback(Output('live-update-table', 'figure'),
              events=[Event('interval-component', 'interval')])

def update_table():
    headerColor = '#119DFF'
    # rowEvenColor = 'lightgrey'
    # rowOddColor = 'white'

    df = pd.read_csv(file_path+'total.csv',encoding='gbk')
    trace = go.Table(
    columnwidth=[0.3, 0.2, 0.3, 0.2, 0.3,
                 0.3, 0.2, 0.3, 0.3, 0.3,
                 0.3, 0.3, 0.3],
        header=dict(
        values=list(df.columns[0:]),
        font=dict(color='white', size=15),
        line = dict(color='rgb(50, 50, 50)'),
        align = 'center',
        fill = dict(color=headerColor),
    ),
    cells=dict(
        values=[df[k].tolist() for k in df.columns[0:]],
        line = dict(color='rgb(50, 50, 50)'),
        font=dict(color='black', size=15),
        height=30,
        align = 'left',
        fill = dict(color='#f5f5fa')
    )
)
    layout = dict(width=1800, height=1000,align = ['center'])
    data = [trace]
    return {'data': data,'layout':layout}

########################################
# execution
########################################

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run_server(debug=False, host='0.0.0.0', port=port)