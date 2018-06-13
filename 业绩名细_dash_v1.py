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
interval = 1/6*minute*second

###############################
# dash board
###############################

app = dash.Dash('auth')
auth = dash_auth.BasicAuth(
    app,
    (('hst', 'fsmeeting2018',),)
)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

app.layout = html.Div(
    html.Div([
        # dcc.Graph(id='live-update-graph-scatter', animate=True),
        dcc.Graph(id='live-update-table0'),
        dcc.Graph(id='live-update-table1'),
        dcc.Graph(id='live-update-table2'),
        dcc.Interval(
            id='interval-component',
            interval=interval
        )
    ])
)


# #table 0
@app.callback(Output('live-update-table0', 'figure'),
              events=[Event('interval-component', 'interval')])

def update_table():
    headerColor = '#119DFF'
    # rowEvenColor = 'lightgrey'
    # rowOddColor = 'white'

    df = pd.read_csv(file_path+'sales_by_team.csv',encoding='gbk')
    trace = go.Table(
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
        font=dict(color='black', size=12),
        height=20,
        align = 'left',
        fill = dict(color='#f5f5fa')
    )
)
    layout = dict(width=1000, height=650, align = ['center'])
    data = [trace]
    return {'data': data,'layout':layout}



# #table 1
@app.callback(Output('live-update-table1', 'figure'),
              events=[Event('interval-component', 'interval')])

def update_table():
    headerColor = '#119DFF'
    # rowEvenColor = 'lightgrey'
    # rowOddColor = 'white'

    df = pd.read_csv(file_path+'sales_figures.csv',encoding='gbk')
    trace = go.Table(
    # columnwidth=[0.3, 0.2, 0.3, 0.2, 0.3,
    #              0.3, 0.2, 0.3, 0.3, 0.3,
    #              0.3, 0.3, 0.3],
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
        font=dict(color='black', size=12),
        height=20,
        align = 'left',
        fill = dict(color='#f5f5fa')
    )
)
    layout = dict(width=1800, height=800,align = ['center'])
    data = [trace]
    return {'data': data,'layout':layout}

# table 2
@app.callback(Output('live-update-table2', 'figure'),
              events=[Event('interval-component', 'interval')])

def update_table():
    headerColor = '#119DFF'
    # rowEvenColor = 'lightgrey'
    # rowOddColor = 'white'

    df = pd.read_csv(file_path+'sales_ranking.csv',encoding='gbk')
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
        font=dict(color='black', size=12),
        height=20,
        align = 'left',
        fill = dict(color='#f5f5fa')
    )
)
    layout = dict(width=1800, height=800,align = ['center'])
    data = [trace]
    return {'data': data,'layout':layout}

########################################
# execution
########################################

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run_server(debug=False, host='0.0.0.0', port=port)