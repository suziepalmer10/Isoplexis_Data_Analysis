import dash
dash.register_page(__name__, title='Clustering')
from dash import dcc, html, Input, Output, callback
import plotly.express as px
from dash import no_update
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff
import plotly.graph_objects as go

centerStyle = {'textAlign': 'center'}


layout = html.Div(
    [   html.H1("Hierarchial Clustering"),
        html.H4("Select subset to view for Hierarchial Clustering"),
        html.P("This selection will change both all cytokine and individual cytokine dendrograms and heatmaps."),
        dcc.RadioItems(id='heatmap_dendro_options', 
                    value="All", style={'textAlign': 'center'},
                      inputStyle={"margin-right": "5px", "margin-left": "5px"}),

        html.H2("Hierarchial Clustering Across All Cytokines"),
        html.H4("Dendrogram and Heatmap are clustered based on cytokine expression value similarities."),
        html.P("Note: the Cell ID in the legend represents the original cell ID of the uploaded data."),

        dbc.Row([dbc.Col(html.Div([
            dcc.Graph(id = 'graph_dendro_all'),
        ])),
        dbc.Col(html.Div([
            dcc.Graph(id = 'graph_hm_all')
        ]))]),

        html.H2("Hierarchial Clustering For Selected Individual Cytokine"),
        html.H4("Dendrogram and Heatmap are clustered based on cytokine expression value similarities."),
        html.P("Note: the Cell ID in the legend represents the original cell ID of the uploaded data."),

        dbc.Row([dbc.Col(html.Div([
            dcc.Graph(id = 'graph_dendro_sub'),
        ])),
        dbc.Col(html.Div([
            dcc.Graph(id = 'graph_hm_sub')
        ]))]),
        html.P("Note: if you would like to view individual cytokine expression of a different cytokine, repeat step 5."),


    ], style = centerStyle
)

#callback for all cytokine heatmap and dendrogram
@callback(
    Output('heatmap_dendro_options', 'options'),
    Input('analysis-button','n_clicks'),
    State('ordered_list', 'value'))
def histdendro_all_callback(n, selected_cytokine): 
    try:
        if n is None: 
            return no_update
        else:
            return ["All"] +selected_cytokine
    except:
        return no_update

@callback(Output('graph_dendro_all', 'figure'),
            Input('analysis-button','n_clicks'),
            Input('cyto_list', 'data'),
            Input('heatmap_dendro_options', 'value'),
            State ('stored-data-reordered', 'data'))
def whole_dendro_cyto(n, cyto_list, option,  df):
    try:
        if n is None: 
            return no_update
        else:
            fig = dendrogram(n, cyto_list, option, df)
            fig.update_layout(title_text="Hierarchial Clustered Dendrogram for All Cytokines", title_x=0.5)
            fig.update_layout(width=700, height=700, plot_bgcolor='rgb(255,255,255)')
            return(fig)
    except:
        return no_update

def dendrogram(n, cyto_list, option, data):
    try:
        if n is None: 
            return no_update
        else:
            data = pd.DataFrame(data)
            if option == "All":
                data = data
            else:
                #subset dataframe based on treatment conditions
                data = data[data["Treatment Conditions"] == option]
            #dendrogram creation
            df_sub = data[cyto_list]
            col_names = list(df_sub.columns)
            #convert transposed df to numpy array
            numpy_array = df_sub.T.to_numpy()
            #numpy_array.shape
            fig = ff.create_dendrogram(numpy_array, orientation='bottom', labels=col_names,
                                colorscale=  px.colors.sequential.Reds_r)
            fig.update_yaxes(showticklabels=False, ticks="")
            fig.update_xaxes(ticks="", showticklabels=False,)
            fig.update_xaxes(showticklabels=True)
            return(fig)
    except:
        return no_update

@callback(Output('graph_hm_all', 'figure'),
            Input('analysis-button','n_clicks'),
            Input('cyto_list', 'data'),
            Input('heatmap_dendro_options', 'value'),
            State ('stored-data-reordered', 'data'))

#these functions perform hierarchial clustering and reordering of the dataframe. 
#From the reorderd dataframe, a heatmap is created 
def sub_heatmap(n, cyto_list, option, df):
    try:
        if n is None: 
            return no_update
        else:
            df = pd.DataFrame(df)
            if option == "All":
                df = df
            else:    
                df = df[df["Treatment Conditions"] == option]
            fig = df_heatmap(n, cyto_list, df)
            fig.update_layout(title_text= "Clustered Heatmap for All Cytokines", title_x=0.5)
            fig.update_layout(width=700, height=700)
            fig.update_yaxes(title_text='Original Cell ID')
            return(fig)
    except:
        return no_update

def df_heatmap(n, cyto_list, df):
    try:
        if n is None: 
            return no_update
        else:
            df = pd.DataFrame(df)
            #keeps cell index even after subsetting, so that correct cells are returned
            index_pos_cells = df['Permanent Index'].tolist()
            str_index_pos_cells = [str(x) for x in index_pos_cells]
            #original list of cytokines to be used for dendrogram
            df_sub = df[cyto_list]
            col_names = list(df_sub.columns)
            #convert transposed df to numpy array - used for dendrogram
            numpy_array = df_sub.T.to_numpy()
            #create dendrogram to be used for reordering of matrix
            dendro_side = ff.create_dendrogram(numpy_array, orientation='right')
            #this gives the index positions of the columns based on dendrogram clustering
            dendro_leaves = dendro_side['layout']['yaxis']['ticktext']
            dendro_leaves = list(map(int, dendro_leaves))
            #this reorders the matrix based on given index positions
            after_dendro_cluster = []
            for i in dendro_leaves:
                after_dendro_cluster.append(col_names[i])
            df_cluster_cyto = df.reindex(columns=after_dendro_cluster)
            data = df_cluster_cyto.to_numpy()
            heatmap = go.Heatmap(z=data, x=after_dendro_cluster, y= str_index_pos_cells, showscale=True, 
            colorscale = px.colors.sequential.Reds, colorbar = dict(title='Value'),
            hovertemplate='Cytokine: %{x}<br>Original Cell ID: %{y}<br>Value: %{z}<extra></extra>')
            fig = go.Figure(heatmap)
            return(fig)
    except:
        return no_update

#callback for individual dendrogram
@callback(Output('graph_dendro_sub', 'figure'),
            Input('indiv-cyto-button','n_clicks'),
            State('indiv_cyto_dropdown', 'value'),
            State('cyto_list', 'data'),
            Input('heatmap_dendro_options', 'value'),
            State ('stored-data-reordered', 'data'))

def sub_dendro_cyto(n, cytokine, cyto_list,  option, df):
    if n is None: 
        return no_update
    else:
        df = pd.DataFrame(df)
        df_cluster = df[df[cytokine] != 0]
        fig = dendrogram(n, cyto_list, option, df_cluster)
        fig.update_layout(title_text= cytokine + " Hierarchial Clustered Dendrogram", title_x=0.5)
        fig.update_layout(plot_bgcolor='rgb(255,255,255)')
        fig.update_layout(width=700, height=700)
        return(fig)


@callback(Output('graph_hm_sub', 'figure'),
            Input('indiv-cyto-button','n_clicks'),
            State('indiv_cyto_dropdown', 'value'),
            State('cyto_list', 'data'),
            Input('heatmap_dendro_options', 'value'),
            State ('stored-data-reordered', 'data'))

def sub_heatmap_cyto(n, cytokine, cyto_list,  option, df):
    if n is None: 
        return no_update
    else:
        df = pd.DataFrame(df)
        df_cluster = df[df[cytokine] != 0]
        if option == "All":
            df_cluster = df_cluster
        else:    
            df_cluster = df_cluster[df_cluster["Treatment Conditions"] == option]
        fig =df_heatmap(n, cyto_list, df_cluster)
        fig.update_layout(title_text=cytokine + " Clustered Heatmap", title_x=0.5)
        fig.update_layout(width=700, height=700)
        fig.update_yaxes(title_text='Original Cell ID')
        return(fig)