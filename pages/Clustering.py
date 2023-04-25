import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
from dash import no_update
import plotly.express as px
from dash import dcc, html, Input, Output, callback
import dash
import dash_bio

centerStyle = {"textAlign": "center"}

# layout = html.Div(
#     [
#         html.H2("Hierarchical Clustering", style=centerStyle),
#         html.Div(
#             [
#                 html.H4("Select subset to view for Hierarchical Clustering"),
#                 html.P(
#                     "This section will change both all cytokine and individual cytokine dendrograms and heatmaps."
#                 ),
#                 dcc.RadioItems(
#                     id="heatmap_dendro_options",
#                     value="All",
#                     style={"textAlign": "center"},
#                     inputStyle={"margin-right": "5px", "margin-left": "5px"},
#                 ),
#             ],
#             className="shadow p-3 mb-5 bg-white rounded",
#         ),
#         html.Div(
#             [
#                 html.H4("Hierarchical Clustering Across All Cytokines"),
#                 html.P(
#                     "Dendrogram and Heatmap are clustered based on cytokine expression value similarities."
#                 ),
#                 html.P(
#                     [
#                         html.I(className="fa fa-sticky-note"),
#                         "Note: the Cell ID in the legend represents the original cell ID of the uploaded data.",
#                     ]
#                 ),
#                 dbc.Row(
#                     [
#                         dbc.Col(
#                             html.Div(
#                                 [
#                                     dcc.Graph(id="graph_dendro_all"),
#                                 ]
#                             )
#                         ),
#                         dbc.Col(html.Div([dcc.Graph(id="graph_hm_all")])),
#                     ]
#                 ),
#             ],
#             className="shadow p-3 mb-5 bg-white rounded",
#         ),
#         html.Div(
#             [
#                 html.H4("Hierarchical Clustering For Selected Individual Cytokine"),
#                 html.P(
#                     "Dendrogram and Heatmap are clustered based on cytokine expression value similarities."
#                 ),
#                 html.P(
#                     [
#                         html.I(className="fa fa-sticky-note"),
#                         "Note: the Cell ID in the legend represents the original cell ID of the uploaded data.",
#                     ]
#                 ),
#                 dbc.Row(
#                     [
#                         dbc.Col(
#                             html.Div(
#                                 [
#                                     dcc.Graph(id="graph_dendro_sub"),
#                                 ]
#                             )
#                         ),
#                         dbc.Col(html.Div([dcc.Graph(id="graph_hm_sub")])),
#                     ]
#                 ),
#                 html.P(
#                     [
#                         html.I(className="fa fa-sticky-note"),
#                         "Note: if you would like to view individual cytokine expression of a different cytokine, repeat step 6.",
#                     ]
#                 ),
#             ],
#             className="shadow p-3 mb-5 bg-white rounded",
#         ),
#     ]
# )


layout = html.Div(
    [
              html.Div(
                  [
                      html.H4("Clustered Heatmap"),
                      html.P(
                          "This option will change both clustered heatmaps."
                      ),
                      dcc.RadioItems(
                          id="heatmap_dendro_options",
                          value="All",
                          style={"textAlign": "center"},
                          inline = True,
                          inputStyle={"margin-right": "5px", "margin-left": "5px"},
                      ),
                  ],
                  className="shadow p-3 mb-5 bg-white rounded",
              ),
     
     
     
     html.Div(
                  [
            
                      html.H4("Select subset to view for Hierarchical Clustering"),
                      html.P(
                          "This section will change both all cytokine and individual cytokine dendrograms and heatmaps."
                      ),
                      dcc.RadioItems(
                           id="cluster_setting",
                           options = [
                               #dict(label = 'Cluster All', value = 'all'),
                                      dict(label = 'Cluster by Cells', value = 'row'),
                                      dict(label = 'Cluster by Cytokines', value = 'column')],
                           
                           value="row",
                           inline = True, 
                           style={"textAlign": "center"},
                           inputStyle={"margin-right": "5px", "margin-left": "5px"},
                       )
                  ],
                  className="shadow p-3 mb-5 bg-white rounded",
              ),
    
    html.Div(
            [
                html.H4("Hierarchical Clustering Across All Cytokines"),
                html.P(
                    "Dendrogram and Heatmap are clustered based on cytokine expression value similarities."
                ),
                html.P(
                    [
                        html.I(className="fa fa-sticky-note"),
                        "Note: the Cell ID in the legend represents the original cell ID of the uploaded data.",
                    ]
                ),
                dbc.Row([
                    dbc.Col(
                    html.Div(
                        [
                            dcc.Graph(id="clustergram_all_fig"),
                        ]
                    ), width = 6),
                    dbc.Col(
                        html.Div(
                        dcc.Graph(id="clustergram_sub_fig"),
                        ), width =6)

                ],
                        
                    ),
                
                
                
            ],
            className="shadow p-3 mb-5 bg-white rounded",
        ),
    
    html.Div(
            [
                html.H4("Hierarchical Clustering Across Individul Cytokine"),
                html.P(
                    "Dendrogram and Heatmap are clustered based on cytokine expression value similarities."
                ),
                html.P(
                    [
                        html.I(className="fa fa-sticky-note"),
                        "Note: the Cell ID in the legend represents the original cell ID of the uploaded data.",
                    ]
                ),
                dbc.Row([
                    dbc.Col(
                    html.Div(
                        [
                            dcc.Graph(id="graph_cluster_individual"),
                        ]
                    ), width = 6),
                    dbc.Col(
                        html.Div(
                        dcc.Graph(id="clustergram_individual_fig"),
                        ), width =6)

                ],
                        
                    ),
                html.P(
                                    [
                                        html.I(className="fa fa-sticky-note"),
                                        "Note: if you would like to view individual cytokine expression of a different cytokine, repeat step 6.",
                                    ]
                                ),
                
                
                
            ],
            className="shadow p-3 mb-5 bg-white rounded",
        ),
        
        

     
     
     
     ]
    )


@callback(
    Output("heatmap_dendro_options", "options"),
    Input("analysis-button", "n_clicks"),
    State("ordered_list", "value"),
)
def histdendro_all_callback(n, selected_cytokine):
    try:
        if n is None:
            return no_update
        else:
            return ["All"] + selected_cytokine
    except:
        return no_update


#callback to cluster all (both sides)
@callback(
    Output("clustergram_all_fig", "figure"),
    Input("analysis-button", "n_clicks"),
    Input("cyto_list", "data"),
    #Input("cluster_setting", "value"),
    #State("stored-data-reordered", "data"),
    State("filtered-data", "data"),
    Input("heatmap_dendro_options", "value"),
)
#def clustergram(n, cyto_list, option, df):
#def clustergram(n, cyto_list, cluster_type, df):
def clustergram(n, cyto_list, df, option):
    try:
        if n is None:
            return no_update
        else:
            return(create_clustergram(n, cyto_list, 'all', df, option, ' Across Cytokines and Cells'))

    except:
        return no_update
    
#callback to cluster either cytokines or cells
#there is a bug in the code for the annotation line
@callback(
    Output("clustergram_sub_fig", "figure"),
    Input("analysis-button", "n_clicks"),
    Input("cyto_list", "data"),
    Input("cluster_setting", "value"),
    #State("stored-data-reordered", "data"),
    State("filtered-data", "data"),
    Input("heatmap_dendro_options", "value"),
)
#def clustergram(n, cyto_list, option, df):
#def clustergram(n, cyto_list, cluster_type, df):
def clustergram_sub(n, cyto_list, clustertype, df, option):
    try:
        if n is None:
            return no_update
        else:
            if clustertype == 'column':
                return(create_clustergram(n, cyto_list, clustertype, df, option, ' Across Cytokines'))
            else:
                return(create_clustergram(n, cyto_list, clustertype, df, option, ' Across Cells'))

    except:
        return no_update    




@callback(
    Output("graph_cluster_individual", "figure"),
    Input("indiv-cyto-button", "n_clicks"),
    State("indiv_cyto_dropdown", "value"),
    State("cyto_list", "data"),
    Input("heatmap_dendro_options", "value"),
    #State("stored-data-reordered", "data"),
    State("filtered-data", "data"),
)
def sub_heatmap_cyto(n, cytokine, cyto_list, option, df):
    try:
        if n is None:
            return no_update
        else:
            df = pd.DataFrame(df)
            df = df[df[cytokine] != 0]
            title = " Across " + cytokine + " Cytokines and Cells"
            return(create_clustergram(n, cyto_list, 'all', df, option, title))

    except:
        return no_update


@callback(
    Output("clustergram_individual_fig", "figure"),
    Input("analysis-button", "n_clicks"),
    Input("indiv-cyto-button", "n_clicks"),
    Input("cyto_list", "data"),
    Input("cluster_setting", "value"),
    #State("stored-data-reordered", "data"),
    State("filtered-data", "data"),
    Input("heatmap_dendro_options", "value"),
    State("indiv_cyto_dropdown", "value"),
)
#def clustergram(n, cyto_list, option, df):
#def clustergram(n, cyto_list, cluster_type, df):
def clustergram_individual(n ,m,  cyto_list, clustertype, df, option, cytokine):
    try:
        if (n is None) and (m is None):
            return no_update
        else:
            if clustertype == 'column':
                df = pd.DataFrame(df)
                df = df[df[cytokine] != 0]
                title = " Across " + cytokine + " Cytokines"
                return(create_clustergram(n, cyto_list, clustertype, df, option, title))
            else:
                df = pd.DataFrame(df)
                df = df[df[cytokine] != 0]
                title = " Across " + cytokine + " Cells"
                return(create_clustergram(n, cyto_list, clustertype, df, option, title))

    except:
        return no_update 
    

    
    
#this function created to fix "bug" in the clustergram code
#this will load the graph twice to ensure the annotation line is the same size
def create_clustergram(n, cyto_list, cluster_type, df, option, title):
            df = pd.DataFrame(df)
            #stores the cell number for heatmap labels
            df['CellNum'] = df.index
            df['CellNum'] += 1
            df['CellNum'] = df['CellNum'].astype(str)
            df['CellNum'] = ' - Cell ' + df['CellNum'].astype(str)
            #cell_number = df.CellNum.values.tolist()
            
            #this is used to select the color for the labels based on treatment conditions
            #color dictionary
            val = df["Treatment Conditions"].unique().tolist()
            colors = ['red', 'green', 'yellow', 'blue', 'orange', 'purple', 'black', 'pink']
            indices = range(0, len(val))
            matched_colors = [colors[i] for i in indices]
           
            
            new_title = "Hierarchical Clustered Heatmap" + title
            
            if option == "All":
                #df2 = df1
                #newdict = result_label
                res = {val[i]: matched_colors[i] for i in range(len(val))}
                C = (pd.Series(df['Treatment Conditions'])).map(res) #convert the list to a pandas series temporarily before mapping
                D= list(C)
                df.set_index('Treatment Conditions')
                df1 = df[cyto_list]
                #this will create cell labels for user
                #new_cell_labels = []
                #for i in range(1, len(D)+1):
                #    new_cell_labels.append(" - Cell " + str(i))
                cell_number = df.CellNum.values.tolist()
                condition = df['Treatment Conditions'].tolist()
                result_label = [i + j for i, j in zip(condition, cell_number)]
            else:
                df = df[df["Treatment Conditions"] == option]
                res = {val[i]: matched_colors[i] for i in range(len(val))}
                C = (pd.Series(df['Treatment Conditions'])).map(res)
                D= list(C)
                df.set_index('Treatment Conditions')
                condition = df['Treatment Conditions'].tolist()
                cell_number = df.CellNum.values.tolist()
                df1 = df[cyto_list]
                result_label = [i + j for i, j in zip(condition, cell_number)]
                
                #newdict = {k: v for k, v in result_label.items() if k.startswith(option)}

            fig = dash_bio.Clustergram(
                data=df1,
                cluster = cluster_type,
                #column_labels=list(df1.columns.values),
                column_labels= cyto_list,
                #column_labels = cyto_list,
                #row_labels=df['Treatment Conditions'].tolist(),
                row_labels = result_label,
                hidden_labels = 'row',
                row_colors = D,
                #hover_data=["x", "y", "z"],
                #labels={'x':'Cytokine', 'y':'Condition and Cell', 'z' :'Intensity'},
                #hovertemplate="Cytokine: %{x}<br>Original Cell ID: %{y}<br>Value: %{z}<extra></extra>",
                color_map= 'Blues',
                #display_ratio=[0.1, 0.7],
                
                #display_ratio=[0.1, 0.7], 
                line_width=2,
                height =700,
                width = 700
                #row_colors_label = 'Treatment Conditions'
            )
            #fig = dendrogram(n, cyto_list, option, df)
            fig.update_layout(
                 title_text=new_title,
                 title_x=0.5,
                         
                 #hovertemplate="Cytokine: %{x}<br>Original Cell ID: %{y}<br>Value: %{z}<extra></extra>"
             )
        
            #fig.update_layout(width=650, height=650)
            fig.update_layout(plot_bgcolor="rgb(255,255,255)")

            return fig
      

# @callback(
#     Output("graph_dendro_all", "figure"),
#     Input("analysis-button", "n_clicks"),
#     Input("cyto_list", "data"),
#     Input("heatmap_dendro_options", "value"),
#     State("stored-data-reordered", "data"),
# )
# def whole_dendro_cyto(n, cyto_list, option, df):
#     try:
#         if n is None:
#             return no_update
#         else:
#             fig = dendrogram(n, cyto_list, option, df)
#             fig.update_layout(
#                 title_text="Hierarchical Clustered Dendrogram for All Cytokines",
#                 title_x=0.5,
#             )
#             # fig.update_layout(width=650, height=650)
#             fig.update_layout(plot_bgcolor="rgb(255,255,255)")
#             return fig
#     except:
#         return no_update


# def dendrogram(n, cyto_list, option, data):
#     try:
#         if n is None:
#             return no_update
#         else:
#             data = pd.DataFrame(data)
#             if option == "All":
#                 data = data
#             else:
#                 # subset dataframe based on treatment conditions
#                 data = data[data["Treatment Conditions"] == option]
#             # dendrogram creation
#             df_sub = data[cyto_list]
#             col_names = list(df_sub.columns)
#             # convert transposed df to numpy array
#             numpy_array = df_sub.T.to_numpy()
#             # numpy_array.shape
#             fig = ff.create_dendrogram(
#                 numpy_array,
#                 orientation="bottom",
#                 labels=col_names,
#                 colorscale=px.colors.sequential.Reds_r,
#             )
#             fig.update_yaxes(showticklabels=False, ticks="")
#             fig.update_xaxes(
#                 ticks="",
#                 showticklabels=False,
#             )
#             fig.update_xaxes(showticklabels=True)
#             return fig
#     except:
#         return no_update


# @callback(
#     Output("graph_hm_all", "figure"),
#     Input("analysis-button", "n_clicks"),
#     Input("cyto_list", "data"),
#     Input("heatmap_dendro_options", "value"),
#     State("stored-data-reordered", "data"),
# )
# # these functions perform Hierarchical clustering and reordering of the dataframe.
# # From the reorderd dataframe, a heatmap is created
# def sub_heatmap(n, cyto_list, option, df):
#     try:
#         if n is None:
#             return no_update
#         else:
#             df = pd.DataFrame(df)
#             if option == "All":
#                 df = df
#             else:
#                 df = df[df["Treatment Conditions"] == option]
#             fig = df_heatmap(n, cyto_list, df)
#             fig.update_layout(
#                 title_text="Clustered Heatmap for All Cytokines", title_x=0.5
#             )
#             # fig.update_layout(width=650, height=650)
#             fig.update_yaxes(title_text="Original Cell ID")
#             return fig
#     except:
#         return no_update


# def df_heatmap(n, cyto_list, df):
#     try:
#         if n is None:
#             return no_update
#         else:
#             df = pd.DataFrame(df)
#             # keeps cell index even after subsetting, so that correct cells are returned
#             index_pos_cells = df["Permanent Index"].tolist()
#             str_index_pos_cells = [str(x) for x in index_pos_cells]
#             # original list of cytokines to be used for dendrogram
#             df_sub = df[cyto_list]
#             col_names = list(df_sub.columns)
#             # convert transposed df to numpy array - used for dendrogram
#             numpy_array = df_sub.T.to_numpy()
#             # create dendrogram to be used for reordering of matrix
#             dendro_side = ff.create_dendrogram(numpy_array, orientation="right")
#             # this gives the index positions of the columns based on dendrogram clustering
#             dendro_leaves = dendro_side["layout"]["yaxis"]["ticktext"]
#             dendro_leaves = list(map(int, dendro_leaves))
#             # this reorders the matrix based on given index positions
#             after_dendro_cluster = []
#             for i in dendro_leaves:
#                 after_dendro_cluster.append(col_names[i])
#             df_cluster_cyto = df.reindex(columns=after_dendro_cluster)
#             data = df_cluster_cyto.to_numpy()
#             heatmap = go.Heatmap(
#                 z=data,
#                 x=after_dendro_cluster,
#                 y=str_index_pos_cells,
#                 showscale=True,
#                 colorscale=px.colors.sequential.Reds,
#                 colorbar=dict(title="Value"),
#                 hovertemplate="Cytokine: %{x}<br>Original Cell ID: %{y}<br>Value: %{z}<extra></extra>",
#             )
#             fig = go.Figure(heatmap)
#             return fig
#     except:
#         return no_update


# # callback for individual dendrogram


# @callback(
#     Output("graph_dendro_sub", "figure"),
#     Input("indiv-cyto-button", "n_clicks"),
#     State("indiv_cyto_dropdown", "value"),
#     State("cyto_list", "data"),
#     Input("heatmap_dendro_options", "value"),
#     State("stored-data-reordered", "data"),
# )
# def sub_dendro_cyto(n, cytokine, cyto_list, option, df):
#     if n is None:
#         return no_update
#     else:
#         df = pd.DataFrame(df)
#         df_cluster = df[df[cytokine] != 0]
#         fig = dendrogram(n, cyto_list, option, df_cluster)
#         fig.update_layout(
#             title_text=cytokine + " Hierarchical Clustered Dendrogram", title_x=0.5
#         )
#         fig.update_layout(plot_bgcolor="rgb(255,255,255)")
#         # fig.update_layout(width=650, height=650)
#         return fig


# @callback(
#     Output("graph_hm_sub", "figure"),
#     Input("indiv-cyto-button", "n_clicks"),
#     State("indiv_cyto_dropdown", "value"),
#     State("cyto_list", "data"),
#     Input("heatmap_dendro_options", "value"),
#     State("stored-data-reordered", "data"),
# )
# def sub_heatmap_cyto(n, cytokine, cyto_list, option, df):
#     if n is None:
#         return no_update
#     else:
#         df = pd.DataFrame(df)
#         df_cluster = df[df[cytokine] != 0]
#         if option == "All":
#             df_cluster = df_cluster
#         else:
#             df_cluster = df_cluster[df_cluster["Treatment Conditions"] == option]
#         fig = df_heatmap(n, cyto_list, df_cluster)
#         fig.update_layout(title_text=cytokine + " Clustered Heatmap", title_x=0.5)
#         # fig.update_layout(width=650, height=650)
#         fig.update_yaxes(title_text="Original Cell ID")
#         return fig
