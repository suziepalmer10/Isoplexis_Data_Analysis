from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
from dash import html, Input, Output, callback, dcc, dash_table
import dash
dash.register_page(__name__, path="/", title='Overview')

centerStyle = {'textAlign': 'center'}
image_path = 'assets/nav_bar.png'
# human single cell adaptive immune table
human_adaptive = {'Functional Groups': ['Effector', 'Stimulatory', 'Chemoattractive', 'Regulatory', 'Inflammatory'],
                  'Cytokines': ['Granzyme B, IFN-g, MIP1-a, Perforin, TNF-a, TNF-b',
                                'GM-CSF, IL-2, IL-5, IL-7, IL-8, IL-9, IL-12, IL-15, IL-21',
                                'CCL11, IP-10, MIP-1B, RANTES',
                                'IL-4, IL-10, IL-13, IL-22, TGF-B1, sCD137, sCD40L',
                                'IL-1B, IL-6, IL-17A, IL-17F, MCP-1, MCP-4'
                                ]}
human_adaptive_table = pd.DataFrame(data=human_adaptive)
human_ad_table = dash_table.DataTable(
    human_adaptive_table.to_dict('records'), [
        {"name": i, "id": i} for i in human_adaptive_table.columns],
    style_data={'whiteSpace': 'normal',
                'height': 'auto', 'lineHeight': '15px'},
    fill_width=False,
    style_cell={'fontSize': 20, 'font-family': 'sans-serif',
                'textAlign': 'left', 'padding': '10px'},
    style_header={'backgroundColor': 'gray', 'fontWeight': 'bold', 'textAlign': 'center'})

# mouse single cell adaptive immune table
mouse_adaptive = {'Functional Groups': ['Effector', 'Stimulatory', 'Chemoattractive', 'Regulatory', 'Inflammatory'],
                  'Cytokines': ['Granzyme B, IFN-g, MIP1-a, TNF-a', 'GM-CSF, IL-2, IL-5, IL-7, IL-12p70, IL-15, IL-18, IL-21, sCD137',
                                'CCL11, CXCL1, CXCL13, IP10, RANTES', 'Fas, IL-4, IL-10, IL-13, IL-27, TGFB1', 'IL-6, IL-17A, MCP-1, IL-1B']}
mouse_adaptive_table = pd.DataFrame(data=mouse_adaptive)
mouse_ad_table = dash_table.DataTable(
    mouse_adaptive_table.to_dict('records'), [
        {"name": i, "id": i} for i in mouse_adaptive_table.columns],
    style_data={'whiteSpace': 'normal',
                'height': 'auto', 'lineHeight': '15px'},
    fill_width=False,
    style_cell={'fontSize': 20, 'font-family': 'sans-serif',
                'textAlign': 'left', 'padding': '10px'},
    style_header={'backgroundColor': 'gray', 'fontWeight': 'bold', 'textAlign': 'center'
                  })

# nhp single cell adaptive immune table
nhp_adaptive = {'Functional Groups': ['Effector', 'Stimulatory', 'Chemoattractive', 'Regulatory', 'Inflammatory'],
                'Cytokines': ['IFN-g, MIP-1a, TNF-a',
                              'GM-CSF, IL-12p70, IL-2',
                              'IL-8, IP-10, RANTES',
                              'IL-4',
                              'IL-1b, IL-6, MCP-1, MIF']}
nhp_adaptive_table = pd.DataFrame(data=nhp_adaptive)
nhp_ad_table = dash_table.DataTable(
    nhp_adaptive_table.to_dict('records'), [
        {"name": i, "id": i} for i in nhp_adaptive_table.columns],
    style_data={'whiteSpace': 'normal',
                'height': 'auto', 'lineHeight': '15px'},
    fill_width=False,
    style_cell={'fontSize': 20, 'font-family': 'sans-serif',
                'textAlign': 'left', 'padding': '10px'},
    style_header={'backgroundColor': 'gray', 'fontWeight': 'bold', 'textAlign': 'center'
                  })


# human single cell inflammation table
human_inflammation = {'Functional Groups': ['TH1 Pro-inflammatory', 'TH2 Pro-inflammatory', 'Chemoattractive',
                                            'Regulatory', 'TH17 Pro-inflammatory', 'Cytolytic', 'Other'],
                      'Cytokines': ['GM-CSF, IFN-g, IL-2, IL-12, TNF-a, TNF-b',
                                    'Il-4, IL-5, IL-7, IL-9, IL-13',
                                    'CCL11, IL-8, IP-10, MCP-1, MCP-4, MIP-1a, MIP-1B, RANTES',
                                    'IL-10, IL-15, IL-22, TGF-B1',
                                    'IL-1B, IL-6, IL-17A, IL-17F, IL-21',
                                    'Granzyme B, Perforin',
                                    'sCD40L, sCD137']}
human_inflammation_table = pd.DataFrame(data=human_inflammation)
human_inflam_table = dash_table.DataTable(
    human_inflammation_table.to_dict(
        'records'), [{"name": i, "id": i} for i in human_inflammation_table.columns],
    style_data={'whiteSpace': 'normal',
                'height': 'auto', 'lineHeight': '15px'},
    fill_width=False,
    style_cell={'fontSize': 20, 'font-family': 'sans-serif',
                'textAlign': 'left', 'padding': '10px'},
    style_header={'backgroundColor': 'gray', 'fontWeight': 'bold', 'textAlign': 'center'
                  })

# human single cell innate immune table
human_innate = {'Functional Groups': ['Effector', 'Stimulatory', 'Chemoattractive', 'Regulatory', 'Inflammatory', 'Growth Factors'],
                'Cytokines': ['IFN-g, MIP-1a, TNF-a, TNF-b',
                              'GM-CSF, IL-8, IL-9, IL-15, IL-18, TGF-a',
                              'CCL11, CXCL13, IP-10, MIP-1B, RANTES',
                              'IL-10, IL-13, IL-22, sCD40L, TGF-B1',
                              'IL-1B, IL-6, IL-12 p40, IL-12 p70, IL-17A, IL-17F, MCP-1, MCP-4, MIF',
                              'EGF, PDGF, VEGF']}
human_innate_table = pd.DataFrame(data=human_innate)
human_inn_table = dash_table.DataTable(
    human_innate_table.to_dict('records'), [
        {"name": i, "id": i} for i in human_innate_table.columns],
    style_data={'whiteSpace': 'normal',
                'height': 'auto', 'lineHeight': '15px'},
    fill_width=False,
    style_cell={'fontSize': 20, 'font-family': 'sans-serif',
                'textAlign': 'left', 'padding': '10px'},
    style_header={'backgroundColor': 'gray', 'fontWeight': 'bold', 'textAlign': 'center'
                  })

header = dbc.Row([dbc.Col(html.Div(
    [
        html.H4(id='check_cyto_num', style={"text-decoration": "underline"}),
        html.P(id='warning1'),
        html.H4(id='row_value'),
        html.H4(id='col_value')
    ]))], style=centerStyle)

instructions = dbc.Row(
    [
        dbc.Row(
            html.H2(dcc.Markdown('''
             *Descriptions of Pages:*
            '''),  style={"text-decoration": "underline", 'textAlign': 'center'})),
        dbc.Row(
            [
                dbc.Col(html.Div(
                    [
                        html.Img(src=image_path, width = "100%"),
                        html.H4(dcc.Markdown('''
            *This is an image of the navigation bar that is found on the top-right corner of this website (You are currently on the Overview Page).*
            ''')),
                    ]
                ), width=4),
                dbc.Col(html.Div(
                    [
                        html.H3(dcc.Markdown('''__*Clustering:*__ displays hierarchical clustered dendrogram and heatmap for all or any individual treatment conditions selected. Clustering across all cytokines is displayed at the top of the page, and the user can also select individual cytokines to cluster, which is displayed at the bottom of the page. ''')),
                        html.H3(dcc.Markdown('''__*Dimensionality Reduction Analysis:*__ displays PCA and tSNE plots across selected treatment conditions. The user can view the data in 3D or 2D and has several options for tSNE optimization parameters, perplexity, and the number of iterations. ''')),
                        html.H3(dcc.Markdown('''__*Polyfunctionality and Dominant Functional Groups:*__ the percent polyfunctional cytokines will allow the user to calculate the percent polyfunctional cells in each treatment condition. The Dominant Functional Groups allow the user to view raw and proportion data for the functional groups, as classified by Isoplexis for each treatment condition. For all analyses on this page, CSV files of the data can be downloaded. ''')),
                        html.H3(dcc.Markdown('''__*Distribution and Statistics:*__ displays percent cytokines secreting for each treatment condition at the top of the page. Additionally, individual cytokine statistics are shown below, allowing the user to view individual statistics for each condition, including all-proportion and zero proportion tests. Individual Cytokine data distribution for each treatment condition is also shown at the bottom of the page. ''')),
                    ]
                ), width=8)
            ])
    ]
)

layout = html.Div(
    [
        header,
        dbc.Row(
            [dbc.Col(html.Div(html.Hr()), width={"size": 8, "offset": 2})]),
        instructions,
        html.H2(dcc.Markdown('''
             *Isoplexis Cytokines and Corresponding Functional Groups*
            '''),  style={"text-decoration": "underline", 'textAlign': 'center'}),
        html.H4('The below cytokine classifications were originally described by Isoplexis Single-Cell and are provided below for convenience.', style=centerStyle),
        html.H5('For more information on these classifications and Isoplexis, click on the link below:', style=centerStyle),
        html.H5(html.A("Link to Isoplexis Website",
                href='https://isoplexis.com/support/analyze-your-data/', target="_blank"), style=centerStyle),
        html.H4('Mouse Single-Cell Adaptive Immune - 28 Cytokines',
                style={"text-decoration": "underline", 'textAlign': 'center'}),
        dbc.Col(html.Div(mouse_ad_table), width={"size": 5, "offset": 4}),
        dbc.Row(
            [dbc.Col(html.Div(html.Hr()), width={"size": 2, "offset": 5})]),
        html.H4('Human Single-Cell Adaptive Immune - 32 Cytokines',
                style={"text-decoration": "underline", 'textAlign': 'center'}),
        dbc.Col(html.Div(human_ad_table), width={"size": 5, "offset": 4}),
        dbc.Row(
            [dbc.Col(html.Div(html.Hr()), width={"size": 2, "offset": 5})]),
        html.H4('Non-human Primate Single-Cell Adaptive Immune - 14 Cytokines',
                style={"text-decoration": "underline", 'textAlign': 'center'}),
        dbc.Col(html.Div(nhp_ad_table), width={"size": 5, "offset": 4}),
        dbc.Row(
            [dbc.Col(html.Div(html.Hr()), width={"size": 2, "offset": 5})]),
        html.H4('Human Single-Cell Inflammation - 32 Cytokines',
                style={"text-decoration": "underline", 'textAlign': 'center'}),
        dbc.Col(html.Div(human_inflam_table), width={"size": 5, "offset": 4}),
        dbc.Row(
            [dbc.Col(html.Div(html.Hr()), width={"size": 2, "offset": 5})]),
        html.H4('Human Single-Cell Innate Immune - 32 Cytokines',
                style={"text-decoration": "underline", 'textAlign': 'center'}),
        dbc.Col(html.Div(human_inn_table), width={"size": 5, "offset": 4}),
        dbc.Row(
            [dbc.Col(html.Div(html.Hr()), width={"size": 2, "offset": 5})]),
        html.H2(dcc.Markdown('''
             *Contact Information:*
            '''),  style={"text-decoration": "underline", 'textAlign': 'center'}),
        html.H5('Questions and comments should be directed towards:',
                style=centerStyle),
        html.H4(dcc.Markdown('''
             __Suzette Palmer:__ *suzette.palmer@utsouthwestern.edu*
            '''),  style={'textAlign': 'center'}),
        html.H4(dcc.Markdown('''
             __Xiaowei Zhan, Ph.D.:__ *xiaowei.zhan@utsouthwestern.edu*
            '''),  style={'textAlign': 'center'}),
        html.H5(
            'Please report any issues or suggestions through the Github link below:', style=centerStyle),

        html.H4(html.A("Suzette Palmer's Github",
                href='https://github.com/suziepalmer10/Isoplexis_Data_Analysis/issues', target="_blank"), style=centerStyle),

    ]
)


@callback(Output('row_value', 'children'),
          Output('col_value', 'children'),
          Output('check_cyto_num', 'children'),
          Output('warning1', 'children'),
          Input('analysis-button', 'n_clicks'),
          Input('cyto_list', 'data'),
          State('stored-data-reordered', 'data'),
          prevent_initial_call=True,)
def col_row_check(n, cyto_list, df):
    if n is None:
        raise PreventUpdate
    else:
        df = pd.DataFrame(df)
        df_sub = df[cyto_list].T
        row, col = df_sub.shape
        numCytokines = 'Number of Cytokines: ' + str(row)
        numCells = 'Number of Cells: ' + str(col)
        check_cyto_num = 'Please ensure that the number of cytokines and the number of cells displayed below are correct before proceeding.'
        warning1 = 'If these numbers are off, double-check your original csv or excel file and also ensure the selected secretome assay is correct.'
        return(numCytokines, numCells, check_cyto_num, warning1)
