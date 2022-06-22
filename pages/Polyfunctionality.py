import dash
dash.register_page(__name__, title = 'Polyfunctionality')
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import numpy as np # pip install numpy
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash import no_update


centerStyle = {'textAlign': 'center'}

    
layout = html.Div ([
            html.H2(id = "title_poly_analysis"),
            html.H4(id='total_polyfunction'),
            dbc.Row(
            [
                dbc.Col(html.Div([dcc.Graph(id="polyfunctional_bar"),
                html.P(id = "instructions_poly_analysis")],
                )),

                dbc.Col(html.Div(html.P("This is where classification polyfunction graph goes."))),
            ])], style = centerStyle)

#polyfunctional graph and number of polyfunctional cells
@callback(Output('polyfunctional_bar', 'figure'),
        Output('total_polyfunction', 'children'),
        Output('title_poly_analysis', 'children'),
        Output('instructions_poly_analysis', 'children'),
        Input('analysis-button','n_clicks'),
        Input('cyto_list', 'data'),
        State('stored-data-reordered', 'data'))

def polyfunctional_bar_ (n, cyto_list, df):
    try:
        if n is None: 
            #return no_update
            raise PreventUpdate
        else:
            total_count = 0
            df = pd.DataFrame(df)
            df_count_labels = []
            df_condition_labels =[]
            df_count_list = []
            for i in df["Treatment Conditions"].unique():
                df_sub = df[df["Treatment Conditions"] == i]
                df_sub_1 = df_sub[cyto_list].T
                row, col = df_sub_1.shape
                count2 = 0
                count3 = 0
                count4 = 0
                count5 = 0
                count_list = []
                count_labels = ["2 Proteins", "3 Proteins", "4 Proteins", "5+ Proteins"]
                condition_labels = [i]*4
                for column_name in df_sub_1.columns:
                    column = df_sub_1[column_name]
                    # Get the count of Zeros in column 
                    if (column == 0).sum() == row:
                        continue
                    elif (column == 0).sum() == row-1:
                        continue
                    elif (column == 0).sum() == row-2:
                        count2 = count2+1
                        total_count = total_count+1
                    elif (column == 0).sum() == row-3:
                        count3 = count3+1
                        total_count = total_count+1
                    elif (column == 0).sum() == row-4:
                        count4 = count4+1
                        total_count = total_count+1
                    else: 
                        count5 =count5+1
                        total_count = total_count+1
                count_list.append(count2/col*100)
                count_list.append(count3/col*100)
                count_list.append(count4/col*100)
                count_list.append(count5/col*100)
                df_count_labels += count_labels
                df_condition_labels += condition_labels
                df_count_list += count_list

            df = pd.DataFrame(list(zip(df_condition_labels, df_count_labels, df_count_list)),
                    columns =['Treatment Conditions', 'Polyfunctionality Percentages', 
                    'Percent Polyfunctional Cytokines Secreting'])
            fig = px.bar(df, x='Treatment Conditions', y ='Percent Polyfunctional Cytokines Secreting', 
                color='Polyfunctionality Percentages', color_discrete_sequence = px.colors.sequential.thermal)
            fig.update_layout(title_text= 'Polyfunctional Cell Overview', title_x = 0.5)
            fig.update_layout(plot_bgcolor='rgb(255,255,255)')
            polyCells = 'Total Number of Polyfunctional Cells:  '+ str(total_count)
            TitleForAnalysis = "Polyfunctional Analysis"
            InstructionsForAnalysis = 'Polyfunctional Cell Overview: calculates the proportion of cells that express two or more proteins.'
            return(fig, polyCells, TitleForAnalysis, InstructionsForAnalysis)
    except:
        return no_update
