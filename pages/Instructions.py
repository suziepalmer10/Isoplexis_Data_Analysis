import dash
dash.register_page(__name__, path="/", title = 'Instructions')
from dash import html, Input, Output, callback
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate


centerStyle = {'textAlign': 'center'}

#https://stackoverflow.com/questions/66637861/how-to-not-show-default-dcc-graph-template-in-dash
#this will hide the graph until user has loaded data

data_analysis = dbc.Row([dbc.Col(html.Div(
            [html.H3(id = 'iso_stats_header'),
            html.H4(id='row_value'),
            html.H4(id='col_value')
            ]))], style = centerStyle)


layout = html.Div(
    [
        data_analysis,
        #dcc.Store(id='analysis-button')
    ]
)

#callback: pca function
@callback(Output('row_value', 'children'),
        Output('col_value', 'children'),
        Output('iso_stats_header', 'children'),
        Input('analysis-button','n_clicks'),
        Input('cyto_list', 'data'),
        State('stored-data-reordered', 'data'))

def col_row_check (n, cyto_list, df):
    if n is None: 
        #return no_update
        raise PreventUpdate
    else:
        df = pd.DataFrame(df)
        for i in df["Treatment Conditions"].unique():
            df_sub = df[df["Treatment Conditions"] == i]
            df_sub_1 = df_sub[cyto_list].T
            row, col = df_sub_1.shape           
        numCytokines = 'Number of Cytokines: ' + str(row)
        numCells = 'Number of Cells: ' + str(col)
        iso_stats_header = 'Isoplexis Data Analysis'
        return(numCytokines, numCells, iso_stats_header)
