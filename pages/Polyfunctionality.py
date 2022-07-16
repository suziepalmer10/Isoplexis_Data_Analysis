from dash import no_update
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback
import dash

options_effector = ['proportions', 'raw']
centerStyle = {'textAlign': 'center'}

layout = html.Div([
    html.H2("Polyfunctional Analysis", style=centerStyle),
    html.Div([
        html.H4(id='total_polyfunction'),
        dcc.Store(id='poly_df'),
        dcc.Store(id='effector_df'),
        dbc.Row(
            [
                dbc.Col(html.Div([dcc.Graph(id="polyfunctional_bar"),
                                html.P(id="instructions_poly_analysis"),
                                html.Button("Download CSV", id="btn_csv1"),
                                dcc.Download(id="poly-download-dataframe-csv")],
                                )),

                dbc.Col(html.Div([
                    dcc.Graph(id="effector_bar"),
                    html.P("Select to view proportional or raw data:"),
                    dcc.RadioItems(
                        id="proportions_or_raw",
                        options=options_effector,
                        value='proportions',
                        inline=True, inputStyle={"margin-right": "5px", "margin-left": "5px"},
                        style=centerStyle),
                    html.P(id="instructions_effector_analysis"),
                    html.Button("Download CSV", id="btn_csv2"),
                    dcc.Download(id="effector-download-dataframe-csv")
                ])),
            ])
        ], className = "shadow p-3 mb-5 bg-white rounded"),
    ])

# polyfunctional graph and number of polyfunctional cells


@callback(Output('polyfunctional_bar', 'figure'),
          Output('total_polyfunction', 'children'),
          Output('instructions_poly_analysis', 'children'),
          Output('poly_df', 'data'),
          Input('analysis-button', 'n_clicks'),
          Input('cyto_list', 'data'),
          State('stored-data-reordered', 'data'))
def polyfunctional_bar_(n, cyto_list, df):
    try:
        if n is None:
            # return no_update
            raise PreventUpdate
        else:
            total_count = 0
            df = pd.DataFrame(df)
            df_count_labels = []
            df_condition_labels = []
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
                count_labels = ["2 Proteins", "3 Proteins",
                                "4 Proteins", "5+ Proteins"]
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
                        count5 = count5+1
                        total_count = total_count+1
                count_list.append(count2/col*100)
                count_list.append(count3/col*100)
                count_list.append(count4/col*100)
                count_list.append(count5/col*100)
                df_count_labels += count_labels
                df_condition_labels += condition_labels
                df_count_list += count_list

            df = pd.DataFrame(list(zip(df_condition_labels, df_count_labels, df_count_list)),
                              columns=['Treatment Conditions', 'Polyfunctionality Percentages',
                              'Percent Polyfunctional Cytokines Secreting'])
            fig = px.bar(df, x='Treatment Conditions', y='Percent Polyfunctional Cytokines Secreting',
                         color='Polyfunctionality Percentages', color_discrete_sequence=px.colors.qualitative.G10)
            fig.update_layout(
                title_text='Percent Polyfunctional Cytokines Secreting', title_x=0.5)
            fig.update_layout(plot_bgcolor='rgb(255,255,255)')
            polyCells = 'Total Number of Polyfunctional Cells:  ' + \
                str(total_count)
            InstructionsForAnalysis = 'Percent Polyfunctional Cytokines Secreting: calculates the proportion of cells that express two or more proteins.'
            return(fig, polyCells, InstructionsForAnalysis, df.to_dict('records'))
    except:
        return no_update


@callback(
    Output("poly-download-dataframe-csv", "data"),
    Input("btn_csv1", "n_clicks"),
    Input('poly_df', 'data'),
    prevent_initial_call=True,
)
def func_csv_poly(n_clicks, df):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "btn_csv1" in changed_id:
        df = pd.DataFrame(df)
        return dcc.send_data_frame(df.to_csv, "polyfunctional.csv")

# effector bar for classification


@callback(Output('effector_bar', 'figure'),
          Output('instructions_effector_analysis', 'children'),
          Output("effector_df", "data"),
          Input('analysis-button', 'n_clicks'),
          Input('proportions_or_raw', 'value'),
          State('cyto_list', 'data'),
          State('effector_list', 'data'),
          State('stored-data-reordered', 'data'))
def effector_bar_(n, view, cyto_list, effector_data, df):
    if n is None:
        return no_update
    else:
        df = pd.DataFrame(df)
        df1 = df[cyto_list]
        m_df = pd.DataFrame.from_dict(
            [effector_data.keys(), effector_data.values()]).T
        # replaces cytokine name with classification
        df1 = df1.rename(columns=dict(zip(m_df[0], m_df[1])))
        # sums the values of similar classifications
        df2 = df1.groupby(level=0, axis=1).sum()
        df2['Treatment Conditions'] = df['Treatment Conditions']
        count = 0
        for i in df2["Treatment Conditions"].unique():
            df_sub = df2[df2["Treatment Conditions"] == i]
            df_sub.drop("Treatment Conditions", inplace=True, axis=1)
            new_df2 = df_sub.sum(axis=0)
            new_val = new_df2/new_df2.sum()
            if count == 0:
                new_df = pd.DataFrame(new_val, columns=[i])
                raw_df = pd.DataFrame(new_df2, columns=[i])
                count = count + 1
            else:
                new_df[i] = new_val
                raw_df[i] = new_df2
        if view == 'raw':
            treatment, effectors, values = changedf(raw_df)
            percentile_list = pd.DataFrame(
                {'Treatment Conditions': treatment, 'Functional Groups': effectors, 'Raw Values': values})
            fig = px.bar(percentile_list, x='Treatment Conditions', y='Raw Values',
                         color='Functional Groups', color_discrete_sequence=px.colors.qualitative.G10)
            fig.update_layout(
                title_text='Dominant Functional Groups', title_x=0.5)
            fig.update_layout(plot_bgcolor='rgb(255,255,255)')
            InstructionsForAnalysis = 'Raw Dominant Functional Groups: displays breakdown of secreting cytokines as classified by Isoplexis.'
            return fig, InstructionsForAnalysis, raw_df.to_dict('records')
        else:
            try:
                treatment, effectors, values = changedf(new_df)
                percentile_list = pd.DataFrame(
                    {'Treatment Conditions': treatment, 'Functional Groups': effectors, 'Proportion': values})
                fig = px.bar(percentile_list, x='Treatment Conditions', y='Proportion',
                             color='Functional Groups', color_discrete_sequence=px.colors.qualitative.G10)
                fig.update_layout(
                    title_text='Dominant Functional Groups', title_x=0.5)
                fig.update_layout(plot_bgcolor='rgb(255,255,255)')
                InstructionsForAnalysis = 'Proportions Dominant Functional Groups: displays proportions of secreting cytokines as classified by Isoplexis.'
                return fig, InstructionsForAnalysis, new_df.to_dict('records')
            # need this portion since will not initially update
            except:
                treatment, effectors, values = changedf(new_df)
                percentile_list = pd.DataFrame(
                    {'Treatment Conditions': treatment, 'Functional Groups': effectors, 'Proportion': values})
                fig = px.bar(percentile_list, x='Treatment Conditions', y='Proportion',
                             color='Functional Groups', color_discrete_sequence=px.colors.qualitative.G10)
                fig.update_layout(
                    title_text='Dominant Functional Groups', title_x=0.5)
                fig.update_layout(plot_bgcolor='rgb(255,255,255)')
                InstructionsForAnalysis = 'Proportions Dominant Functional Groups: displays proportions of secreting cytokines as classified by Isoplexis.'
                return fig, InstructionsForAnalysis, new_df.to_dict('records')


def changedf(new_df):
    values = new_df.to_numpy().flatten()
    list_a = list(new_df.columns)
    effect = list(new_df.index)
    val = len(values)
    list_size = len(list_a)
    range = val/list_size
    treatment = list_a*int(range)
    class_ = len(effect)
    val2 = val/class_
    effectors = effect*int(val2)
    return(treatment, effectors, values)

# https://stackoverflow.com/questions/62671226/plotly-dash-how-to-reset-the-n-clicks-attribute-of-a-dash-html-button


@callback(
    Output("effector-download-dataframe-csv", "data"),
    Input("btn_csv2", "n_clicks"),
    Input('effector_df', 'data'),
    prevent_initial_call=True,
)
def func_csv_poly(n_clicks, df):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "btn_csv2" in changed_id:
        df = pd.DataFrame(df)
        return dcc.send_data_frame(df.to_csv, "effector.csv")
