import dash
dash.register_page(__name__, title = "Dimensionality Reduction")
from dash import dcc, html, Input, Output, callback
import plotly.express as px
from dash import no_update
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from sklearn.manifold import TSNE


#methods for PCA and TSNE
method_pcatsne = ["Standard Scalar Normalized", "Not Normalized"]
#values neccessary for tsne function
iterations = [250, 300, 400, 500, 600, 700, 800, 900, 1000]
perplexity = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]


centerStyle = {'textAlign': 'center'}

layout = html.Div(
    [   html.H2("Dimensionality Reduction"),
        html.H5("Include PCA and TSNE parameters."),
        html.P("Note: TSNE might take a minute to reload since this is calculated in real-time."),

        dbc.Row([dbc.Col(html.Div([  
                html.Div(dcc.Graph(id='dim_red_fig')),
                dcc.RadioItems(
                    id="method_radio",
                    options=method_pcatsne,
                    value="Standard Scalar Normalized",
                    inline=True, inputStyle={"margin-right": "5px", "margin-left": "5px"}, 
                    style=centerStyle),  
                ])), 
        dbc.Col(html.Div([  
                html.Div(dcc.Graph(id='ts_dim_red_fig')), 
                dcc.RadioItems(
                    id="method_radio1",
                    options=method_pcatsne,
                    value="Standard Scalar Normalized",
                    inline=True, inputStyle={"margin-right": "5px", "margin-left": "5px"}, 
                    style=centerStyle),
                html.P("Select Perplexity of Nearest Neighbors: ", style=centerStyle),
                dcc.RadioItems(
                    id="perplexity_radio",
                    options=perplexity,
                    value=30,
                    inline=True, inputStyle={"margin-right": "5px", "margin-left": "5px"}, 
                    style=centerStyle),
                html.P("Select Number of TSNE Iterations: ", style=centerStyle),
                dcc.RadioItems(
                    id="iterations_radio",
                    options=iterations,
                    value=500,
                    inline=True, inputStyle={"margin-right": "5px", "margin-left": "5px"}, 
                    style=centerStyle)
                ]))])
    ], style = centerStyle
)

#callback: pca function
@callback(Output('dim_red_fig', 'figure'),
            Input('analysis-button','n_clicks'),
            Input('method_radio', 'value'),
            Input('cyto_list', 'data'),
            State ('stored-data-reordered', 'data'), 
            State ('color_discrete_map', 'data'))

def pca_func(n, method, cytokines, df, color_discrete_map):
    if n is None: 
        return no_update
    else:
        df = pd.DataFrame(df)
        x = df[cytokines]
        x = x.to_numpy()
        Y = df['Treatment Conditions']
        Y.to_frame()
        pca = PCA()
        if method == "Standard Scalar Normalized":
            pipe = Pipeline([('scaler', StandardScaler()), ('pca', pca)])
            Xt = pipe.fit_transform(x)
        else:
            Xt = pca.fit_transform(x)
        df = pd.DataFrame(Xt)
        df['Treatment Conditions'] = Y
        fig = px.scatter(df, x=0, y=1, color="Treatment Conditions", color_discrete_map = color_discrete_map)
        fig.update_layout(title_text = method+" PCA", title_x=0.5, )
        fig.update_layout(plot_bgcolor='rgb(255,255,255)')
        fig.update_xaxes(title_text='PCA 1')
        fig.update_yaxes(title_text='PCA 2') 
        return(fig)


#callback: tsne function
@callback(Output('ts_dim_red_fig', 'figure'),
            Input('analysis-button','n_clicks'),
            Input('method_radio', 'value'),
            Input('perplexity_radio', 'value'),
            Input('iterations_radio', 'value'),
            Input('cyto_list', 'data'),
            State ('stored-data-reordered', 'data'), 
            State ('color_discrete_map', 'data'))

def tsne_func(n, method, perplexity, iterations, cyto_list, df, color_discrete_map):
    if n is None: 
        return no_update
    else:
        df= pd.DataFrame(df)
        x = df[cyto_list]
        x = x.to_numpy()
        Y = df['Treatment Conditions']
        Y.to_frame()
        pca = PCA()
        if method == "Standard Scalar Normalized":
            pipe = Pipeline([('scaler', StandardScaler()), ('pca', pca)])
            Xt = pipe.fit_transform(x)
        else:
            Xt = pca.fit_transform(x)
        tsne = TSNE(n_components=2, perplexity=perplexity, n_iter=iterations)
        tsne_results = tsne.fit_transform(Xt)
        df = pd.DataFrame(tsne_results)
        df['Treatment Conditions'] = Y
        fig = px.scatter(df, x=0, y=1, color="Treatment Conditions", color_discrete_map = color_discrete_map)
        fig.update_layout(title_text = method+" TSNE", title_x=0.5, )
        fig.update_layout(plot_bgcolor='rgb(255,255,255)')
        fig.update_xaxes(title_text='TSNE 1')
        fig.update_yaxes(title_text='TSNE 2') 
        return(fig)
