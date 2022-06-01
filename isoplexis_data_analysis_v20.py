#Version20
##required packages
import dash
from dash.dependencies import Input, Output
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from itertools import chain
import plotly.figure_factory as ff
import scipy
import dash_bootstrap_components as dbc
from skimage import io
import numpy as np 
from statsmodels.stats.proportion import proportions_ztest
from scipy.stats import ks_2samp
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.manifold import TSNE

#accepts excel or csv files
#converts file to pandas dataframe
def uploadFile(Path_):
    if Path_.endswith(".xlsx"):
        df = pd.DataFrame(pd.read_excel(Path_))
        df = df.to_csv ("data.csv", index = None, header=True)
        df = pd.DataFrame(pd.read_csv("data.csv"))
    else:
        df = pd.DataFrame(pd.read_csv(Path_))
    return(df)
#file to upload
#df_ = uploadFile("/Users/suziepalmer/Desktop/IsoplexisV9/data.csv")
#df_ = uploadFile("/Users/suziepalmer/Desktop/IsoplexisV9/ABX_ICT_TDLN_121221_CD3+_raw_data.csv")
df_ = uploadFile("/Users/suziepalmer/Desktop/IsoplexisV9/WT_ABX_MLN_T_Cell_CD4+_CD8+_raw_data.csv")

#this is the original cytokine list
cyto_list = ['BCA-1', 'CCL-11', 'FAS', 'GM-CSF', 'Granzyme B', 
    'IFN-g', 'IL-10', 'IL-12p70', 'IL-13', 'IL-15', 'IL-17A', 
    'IL-18', 'IL-1b', 'IL-2', 'IL-21', 'IL-27', 'IL-4', 
    'IL-5', 'IL-6', 'IL-7', 'IP-10', 'KC', 'MCP-1', 'MIP-1a', 
    'RANTES', 'sCD137', 'TGF-b', 'TNF-a']
#this is the original description list
description_list = ["Donor", "Cell Subset", "Stimulation"]
#this column creates a new column which combines all of the descriptions
df_['Treatment Conditions'] = df_[description_list].apply(
    lambda x: ' '.join(x.dropna().astype(str)),
    axis=1)

##create an edited cytokine list for dropdown 
##columns with no values will be removed
edit_cyto_list = []
for i in cyto_list:
    if df_[i].sum() == 0:
        continue
    else: 
        edit_cyto_list.append(i)
#this will be used as the initial value for the dropdown menu
new_val = edit_cyto_list[0]

#below list is used for heatmap/dendrogram of all cytokines
unique_variables = df_["Treatment Conditions"].unique().tolist()
heatmap_options = ["All"]+ unique_variables
###create dictionary for dynamic callbacks for dendrogram and heatmap
heatmap_dictionary = []
for cytokine in edit_cyto_list:
    small_list = ["All"]
    for i in unique_variables: 
        sub_vals  = df_.loc[df_["Treatment Conditions"] == i, cytokine]
        if sub_vals.sum() != 0:
            index = unique_variables.index(i)
            small_list.append(i)
    heatmap_dictionary.append(small_list)
# using dictionary comprehension to convert lists to dictionary
#main dictionary used for the callbacks. 
cytokine_dictionary = {edit_cyto_list[i]: heatmap_dictionary[i] for i in range(len(edit_cyto_list))}

#color schemes used for the bar plots, density, histogram
#"blue", "red", "gray", "green", "yellow", "teal", "purple", "black"
colors = ['rgb(255, 0, 0)', 'rgb(0, 0, 255)', 'rgb(128, 128, 128)', 'rgb(0, 128, 0)', 
         'rgb(255, 255, 0)', 'rgb(0, 128, 128)', 'rgb(128, 0, 128)', 'rgb(0, 0, 0)']
#this makes sure colors are the same for bar plots, density and histogram
num_colors = len(unique_variables)
colors_for_plot = colors[:num_colors]
color_discrete_map = {unique_variables[i]: colors_for_plot[i] for i in range(len(unique_variables))}
#heatmap colors
colors_list_heat = ["gray", "red", "blue", "gray", "green", "yellow", "teal", "purple", "black"]
#bins used for the histogram 
bins = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
#heatmap index positions maintained for cells
num_cells = range(1, len(df_)+1)
df_['Permanent Index'] = num_cells

#methods for PCA and TSNE
method_pcatsne = ["Standard Scalar Normalized", "Not Normalized"]
#values neccessary for tsne function
iterations = [250, 300, 400, 500, 600, 700, 800, 900, 1000]
perplexity = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

##############################
#Non-zero Proportions Graph for All Cytokines
#this produces a NZ Proportion dataframe
def non_zero_prop_table(df, subtypes):
    cyto_list_copy = cyto_list.copy()
    cyto_list_copy.insert(0, subtypes)
    df_1 = df_[cyto_list_copy] 
    list_large = []
    col_names = df_1.columns.tolist()
    col_names.remove(subtypes)
    df_values = pd.DataFrame(cyto_list, columns = ["Cytokines"] )
    for i in df_1[subtypes].unique().tolist():
        list_sub = []
        sub_df = df_1.loc[df_1[subtypes] == i]
        sub_df.pop(subtypes)
        for column in sub_df:
            new_val = ((sub_df[column] != 0).sum())/len(sub_df[column])
            list_sub.append(new_val)
        df_values[str(i)] = list_sub
    return(df_values)
df_val = non_zero_prop_table(df_, "Treatment Conditions")
###this reformats the NZ Proportions dataframe, so that the bar graph can be produced
df_edit =pd.melt(df_val, id_vars=["Cytokines"],var_name='Treatment Conditions', 
                 value_name = 'Percent Cytokine Secreting')
###This plots all of the Cytokines
bar_ALL = px.bar(df_edit, x="Cytokines", color="Treatment Conditions",
    y='Percent Cytokine Secreting',
    #title="Non-Zero Proportions for all Isoplexis Cytokines",
    barmode='group', color_discrete_map = color_discrete_map,
    height=500)
bar_ALL.update_layout(plot_bgcolor='rgb(255,255,255)')
##############################
#Data Analysis Variables
#variable for the file information
len_df = str(len(df_))
df_cyto = df_[cyto_list]
#number of cells and cytokines
def get_num(axis_):
    cell_sub = df_cyto.sum(axis=axis_).tolist()
    cell_sub = [i for i in cell_sub if i != 0]
    return(len(cell_sub))
def cell_unique_val(num):    
    val_list =[]
    df_cyto_t = df_cyto.T
    for col in df_cyto_t:
        val = df_cyto_t[col].value_counts()[0]
        unique_val = len(cyto_list)- val
        val_list.append(unique_val)
    if val <=2:
        unique_val = [i for i in val_list if i == num]
    else:
        unique_val = [i for i in val_list if i >= num]
    return(len(unique_val))

cyto_num = str(len(cyto_list))
pos_cyto = str(get_num(0))
pos_cells1 = str(get_num(1))
poscell_p1 = str(cell_unique_val(1))
poscell_p2 = str(cell_unique_val(2))
poscell_p3 = str(cell_unique_val(3))
##############################

##############################
#Beginning of html Script
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(

    [
        # row 1 - header
        dbc.Row(dbc.Col(html.Div([
        html.H1(dcc.Markdown('''
            **Isoplexis Data Analysis**
            '''), style={'textAlign': 'center'}),
        html.H2('Suzette Palmer - Zhan and Koh Labs', style={'textAlign': 'center'}),
        html.H3('University of Texas Southwestern Medical Center', style={'textAlign': 'center'}),
        html.H3('')]))),
        #row 2 line
        dbc.Row([dbc.Col(html.Div(html.Hr()), width={"size": 8, "offset": 2})]),
        #row 3 - file statistics and information
        dbc.Row([dbc.Col(html.Div(
        [html.H4('Isoplexis Data Analysis File Information:', style={'textAlign': 'center'}),
        html.Div(html.P('Number of Cytokines: ' + cyto_num, style={'textAlign': 'center'})),
        html.Div(html.P('Number of Cytokines With Greater Than One Measurement:  ' + pos_cyto, style={'textAlign': 'center'})),
        html.Div(html.P('Number of Cells Analyzed: ' + len_df, style={'textAlign': 'center'})),
        html.Div(html.P('Number of Cells With At least One Positive Measurement: ' + pos_cells1, style={'textAlign': 'center'})),
        html.Div(html.P('Number of Cells With Exactly One Measurement: ' + poscell_p1, style={'textAlign': 'center'})),
        html.Div(html.P('Number of Cells With Exactly Two Measurements: ' + poscell_p2, style={'textAlign': 'center'})),
        html.Div(html.P('Number of Cells With Three or Greater Measurements: ' + poscell_p3, style={'textAlign': 'center'})),
        html.Div(html.P(''))
        ]))]),   
        #row 4 - line
        dbc.Row([dbc.Col(html.Div(html.Hr()), width={"size": 8, "offset": 2})]),
        ##row 5 - dropdown for dendrogram and clustermap all cytokines
        dbc.Row([dbc.Col(html.Div([
        html.H4("Dendrogram and Clustered Heatmap for All Cytokines", style={'textAlign': 'center'}),
        html.P("Select Which Dendrogram and Corresponding Clustered Heatmap to Display", 
               style={'textAlign': 'center'}),
        dcc.Dropdown(
        id="dropdown_cyto_hm_all",
        options=heatmap_options,
        value="All",
        clearable=False)]), width={"size": 6, "offset": 3})]),
        ##row 6 - dendrogram and clustered Heatmap - all cytokines        
        dbc.Row([  
                dbc.Col(html.Div([dcc.Graph(id='graph_dendro_all')])),
                dbc.Col(html.Div([dcc.Graph(id="graph_hm_all")]))]),
        ##row 7 - line
        dbc.Row([dbc.Col(html.Div(html.Hr()), width={"size": 6, "offset": 3})]),
        ##row 8 - NZ Proportions bar graph for all cytokines
        dbc.Row([
            dbc.Col(html.Div([
        html.H4("Percent Cytokine Secreting Across All Cytokines", style={'textAlign': 'center'}),
        dcc.Graph(figure=bar_ALL)]))]),
        ##row 9 - line
        dbc.Row([dbc.Col(html.Div(html.Hr()), width={"size": 8, "offset":2})]),
        #row 10 - dimensionality reduction analysis
        dbc.Row(
        dbc.Col(html.Div([
        html.H4("Dimensionality Reduction Analysis", style={'textAlign': 'center'})]))),
            dbc.Row([
             dbc.Col(html.Div([  
                html.Div(dcc.Graph(id='dim_red_fig')),
                dcc.RadioItems(
                id="method_radio",
                options=method_pcatsne,
                value="Standard Scalar Normalized",
                inline=True, inputStyle={"margin-right": "5px", "margin-left": "5px"}, 
                style={'textAlign': 'center'}),  
                ])), 
             dbc.Col(html.Div([  
                html.Div(dcc.Graph(id='ts_dim_red_fig')), 
                dcc.RadioItems(
                id="method_radio1",
                options=method_pcatsne,
                value="Standard Scalar Normalized",
                inline=True, inputStyle={"margin-right": "5px", "margin-left": "5px"}, 
                style={'textAlign': 'center'}),
                html.P(""),
                html.P("Select Perplexity of Nearest Neighbors: ", style={'textAlign': 'center'}),
                dcc.RadioItems(
                id="perplexity_radio",
                options=perplexity,
                value=30,
                inline=True, inputStyle={"margin-right": "5px", "margin-left": "5px"}, 
                style={'textAlign': 'center'}),
                html.P(""),
                html.P("Select Number of TSNE Iterations: ", style={'textAlign': 'center'}),
                dcc.RadioItems(
                id="iterations_radio",
                options=iterations,
                value=500,
                inline=True, inputStyle={"margin-right": "5px", "margin-left": "5px"}, 
                style={'textAlign': 'center'})
                ]))]),
        ##row 11 - line
        dbc.Row([dbc.Col(html.Div(html.Hr()), width={"size": 8, "offset":2})]),
        #row 12 - cytokine dropdown
        dbc.Row(dbc.Col(html.Div([
        html.H3("Individual Cytokine Analysis", style={'textAlign': 'center'}),
        html.P("Select One Cytokine to View Data Distribution", 
                   style={'textAlign': 'center'}),
        dcc.Dropdown(
        id='dropdown',
        options=[{'label': k, 'value': k} for k in cytokine_dictionary.keys()],
        value=new_val, clearable=False),
        html.P(" ")
        ]), 
        width={"size": 6, "offset": 3})),
        #row 13 - individual cytokine statistics
        dbc.Row(
        dbc.Col(html.Div([
        html.P(" "),
        html.H4("Cytokine Statistics", style={'textAlign': 'center'}),
        dcc.RadioItems(
        id="dropdown_stat",
        options=heatmap_options,
        value="All",
        inline=True, inputStyle={"margin-right": "5px", "margin-left": "5px"}, 
        style={'textAlign': 'center'}),
        html.P(" "),
        html.Div(id='value_sum', style={'textAlign': 'center'}),
        html.Div(id='zero_sum', style={'textAlign': 'center'}),
        html.Div(id='mean_std_all', style={'textAlign': 'center'}),
        html.Div(id='min_max_all', style={'textAlign': 'center'}),
        html.Div(id='mean_std_nz', style={'textAlign': 'center'}),
        html.Div(id='min_max_nz', style={'textAlign': 'center'}),
        html.P(" ")
        ]), width={"size": 4, "offset": 4})),   
        #row 14 - line
        dbc.Row([dbc.Col(html.Div(html.Hr()), width={"size": 4, "offset": 4})]),
        #row 15 - Statistical tests for individual cytokines
        dbc.Row(
        dbc.Col(html.Div([
        html.H4("Statistical Tests for Differences in Cytokine Secretion", style={'textAlign': 'center'}),
        html.P(dcc.Markdown('''_Select Condition 1:_
        '''), style={'textAlign': 'center'}),
        dcc.Dropdown(id="option_1_stat", options=unique_variables,
                    value=unique_variables[0], clearable=False),
        html.P(" "),
        html.P(dcc.Markdown('''_Select Condition 2:_
        '''), style={'textAlign': 'center'}),
        dcc.Dropdown(id="option_2_stat", options=unique_variables,
                    value=unique_variables[1], clearable=False),
        html.P(" "),
        # NZ Proportion Stats Call
        html.P(dcc.Markdown('''**Percent Cytokine Secreting - Proportion Test**
        '''), style={'textAlign': 'center'}),
        html.Div(id='stats_nz', style={'textAlign': 'center'}),
        html.Div( id='p_val_nz', style={'textAlign': 'center'}),
        html.P(" "),
        # KS Test
        html.P(dcc.Markdown('''**Kolmogorov-Smirnov Test**
        '''), style={'textAlign': 'center'}),
        html.Div(id='stats_ks' , style={'textAlign': 'center'}),
        html.Div( id='p_val_ks', style={'textAlign': 'center'}),
        html.P(" ")]), 
        width={"size": 4, "offset": 4})),
        ##row 16 - space
        dbc.Row([dbc.Col(html.Div(html.Hr()), width={"size": 6, "offset": 3})]),
        ##row 17 - dendrogram and clustered heatmap individual cytokines
        dbc.Row(dbc.Col(html.Div([
        html.H3("Individual Cytokine Data Visualization", style={'textAlign': 'center'}),
        html.P(" "),
        html.P("Select Which Dendrogram and Corresponding Clustered Heatmap to Display", 
                   style={'textAlign': 'center'}),
        dcc.RadioItems(id='heatmap_dropdown', 
                    value="All", style={'textAlign': 'center'},
                      inputStyle={"margin-right": "5px", "margin-left": "5px"}),
        ]), width={"size": 6, "offset": 3})),
        ##########################
        ##row 18 - dendrogram, clustermap and NZ Proportions graph
        dbc.Row(
            [
                dbc.Col(html.Div([dcc.Graph(id="dendro_sub")])),
                dbc.Col(html.Div([dcc.Graph(id="graph4")])),
                dbc.Col(html.Div([dcc.Graph(id="graph1")]))]),
        ##row 19 - space
        dbc.Row([dbc.Col(html.Div(html.Hr()), width={"size": 6, "offset": 3})]),
        #row 20 histogram and density plot
        dbc.Row(
            [dbc.Col(html.Div([
        dcc.Graph(id="graph2"),
        html.P("Select Bin Size", style={'textAlign': 'center'}),
        dcc.RadioItems(
        id="dropdown2",
        options=bins,
        value=20,
        style={'textAlign': 'center'}, inputStyle={"margin-right": "5px", "margin-left": "5px"}),
        html.P("  "),
        html.P("Select Box Plot, Violin Plot or Rug Plot:", style={'textAlign': 'center'}),
        dcc.RadioItems(
        id='distribution',
        options=[{'label':'Box Plot', 'value':'box'}, {'label':'Violin Plot', 'value':'violin'}, 
                 {'label':'Rug Plot','value': 'rug'}],
        value='box', inline=True, inputStyle={"margin-right": "5px", "margin-left": "5px"}, 
            style={'textAlign': 'center'}),
        html.P("  ")])),
        dbc.Col(html.Div([
        dcc.Graph(id="graph3")]))]),
])

######call back functions
#callback: pca function
@app.callback(Output('dim_red_fig', 'figure'),
              [Input('method_radio', 'value')])

def pca_func(method):
    x = df_[cyto_list]
    features = x.columns
    x = x.to_numpy()
    Y = df_['Treatment Conditions']
    Y.to_frame()
    pca = PCA()
    if method == "Standard Scalar Normalized":
        pipe = Pipeline([('scaler', StandardScaler()), ('pca', pca)])
        Xt = pipe.fit_transform(x)
    else:
        Xt = pca.fit_transform(x)
    df = pd.DataFrame(Xt)
    df['Treatment Conditions'] = Y
    fig = px.scatter(df, x=0, y=1, color="Treatment Conditions", color_discrete_map = color_discrete_map, 
                    )
    fig.update_layout(title_text = method+" PCA", title_x=0.5, )
    fig.update_layout(plot_bgcolor='rgb(255,255,255)')
    fig.update_xaxes(title_text='PCA 1')
    fig.update_yaxes(title_text='PCA 2') 
    return(fig)
#callback tsne function
@app.callback(Output('ts_dim_red_fig', 'figure'),
              [Input('method_radio1', 'value')],
            [Input('perplexity_radio', 'value')],
             [Input('iterations_radio', 'value')])

def tsne_func(method, perplexity_, iterations_):
    x = df_[cyto_list]
    features = x.columns
    x = x.to_numpy()
    Y = df_['Treatment Conditions']
    Y.to_frame()
    pca = PCA()
    if method == "Standard Scalar Normalized":
        pipe = Pipeline([('scaler', StandardScaler()), ('pca', pca)])
        Xt = pipe.fit_transform(x)
    else:
        Xt = pca.fit_transform(x)
    tsne = TSNE(n_components=2, perplexity=perplexity_, n_iter=iterations_)
    tsne_results = tsne.fit_transform(Xt)
    df = pd.DataFrame(tsne_results)
    df['Treatment Conditions'] = Y
    fig = px.scatter(df, x=0, y=1, color="Treatment Conditions", color_discrete_map = color_discrete_map)
    fig.update_layout(title_text = method+" TSNE", title_x=0.5, )
    fig.update_layout(plot_bgcolor='rgb(255,255,255)')
    fig.update_xaxes(title_text='TSNE 1')
    fig.update_yaxes(title_text='TSNE 2') 
    return(fig)
#callback: all cytokine dendrogram
@app.callback(Output('graph_dendro_all', 'figure'),
              [Input('dropdown_cyto_hm_all', 'value')])

def whole_dendro_cyto(option):
    df_cluster = df_.copy()
    fig = dendrogram(option, df_cluster)
    fig.update_layout(title_text="Hierarchial Clustered Dendrogram for All Cytokines", title_x=0.5)
    fig.update_layout(width=700, height=700, plot_bgcolor='rgb(255,255,255)')
    return(fig)

def dendrogram(option, data):
    new_color_list = []
    #df_cluster = df_.copy()
    if option == "All":
        data = data
    else:
        #subset dataframe based on treatment conditions
        data = data[data["Treatment Conditions"] == option]
    #get color from the index position
    index = heatmap_options.index(option)
    color_ = colors_list_heat[index]
    #need to create an array of size 8 with the updated color for the plot
    for i in range(8):
        new_color_list.append(color_)
    #dendrogram creation
    df_sub = data[cyto_list]
    col_names = list(df_sub.columns)
    #convert transposed df to numpy array
    numpy_array = df_sub.T.to_numpy()
    #numpy_array.shape
    fig = ff.create_dendrogram(numpy_array, orientation='bottom', labels=col_names,
                         colorscale =  new_color_list)
    fig.update_yaxes(showticklabels=False, ticks="")
    fig.update_xaxes(ticks="", showticklabels=False,)
    fig.update_xaxes(showticklabels=True)
    return(fig)
#call back: all cytokine heatmap
@app.callback(Output('graph_hm_all', 'figure'),
              [Input('dropdown_cyto_hm_all', 'value')])
#these functions perform hierarchial clustering and reordering of the dataframe. 
#From the reorderd dataframe, a heatmap is created 
def sub_heatmap(option):
    df_cluster = df_.copy()
    if option == "All":
        df_cluster = df_cluster
    else:    
        df_cluster = df_cluster[df_cluster["Treatment Conditions"] == option]
    index = heatmap_options.index(option)
    color_ = colors_list_heat[index]
    fig = df_heatmap(df_cluster, color_)
    fig.update_layout(title_text= "Clustered Heatmap for All Cytokines", title_x=0.5)
    fig.update_layout(width=700, height=700)
    return(fig)

def df_heatmap(df, color):
    #keeps cell index even after subsetting, so that correct cells are returned
    index_pos_cells = df['Permanent Index'].tolist()
    df = df[cyto_list]
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
    df_cluster_cyto_arr = df_cluster_cyto.to_numpy()
    data=df_cluster_cyto_arr
    heatmap = px.imshow(data,
            labels=dict(x="Cytokines", y="Cells", color="Value"),
                x=after_dendro_cluster ,
                y= index_pos_cells,
                #color_continuous_scale='Greys'
                color_continuous_scale=["white", color])
    heatmap.update_xaxes(side="bottom")
    return(heatmap)
#callback for individual cytokine dropdown and heatmap dropdown
@app.callback(
    dash.dependencies.Output('heatmap_dropdown', 'options'),
    [dash.dependencies.Input('dropdown', 'value')])
def cytokine_callback(selected_cytokine):   
    return [{'label': i, 'value': i} for i in cytokine_dictionary[selected_cytokine]]
#call back for heatmap 
@app.callback(
    dash.dependencies.Output('graph4', 'figure'),
    [dash.dependencies.Input('dropdown', 'value'),
     dash.dependencies.Input('heatmap_dropdown', 'value')])
def sub_heatmap_cyto(cytokine, option):
    df_cluster = df_[df_[cytokine] != 0]
    if option == "All":
        df_cluster = df_cluster
    else:    
        df_cluster = df_cluster[df_cluster["Treatment Conditions"] == option]
    index = heatmap_options.index(option)
    color_ = colors_list_heat[index]
    fig = df_heatmap(df_cluster, color_)
    fig.update_layout(title_text=cytokine + " Clustered Heatmap", title_x=0.5)
    return(fig)
#callback for individual dendrogram 
@app.callback(
    dash.dependencies.Output('dendro_sub', 'figure'),
    [dash.dependencies.Input('dropdown', 'value'),
     dash.dependencies.Input('heatmap_dropdown', 'value')])

def sub_dendro_cyto(cytokine, option):
    df_cluster = df_[df_[cytokine] != 0]
    fig = dendrogram(option, df_cluster)
    fig.update_layout(title_text= cytokine + " Hierarchial Clustered Dendrogram", title_x=0.5)
    fig.update_layout(plot_bgcolor='rgb(255,255,255)')
    return(fig)
#callback bargraph
@app.callback(
    dash.dependencies.Output("graph1", "figure"),
    [dash.dependencies.Input('dropdown', 'value')])

def update_bar_chart(cytokine):
    df = df_edit
    mask = df["Cytokines"] == cytokine
    fig = px.bar(df[mask], x="Treatment Conditions", y="Percent Cytokine Secreting", 
        color="Treatment Conditions", color_discrete_map = color_discrete_map, barmode="group",
        #title = cytokine + " Non-Zero Proportions", 
        text_auto = True)
    fig.update_layout(title_text=cytokine + " Percent Cytokine Secreting", title_x=0.5)
    fig.update_layout(plot_bgcolor='rgb(255,255,255)')
    return fig
#callback - individual cytokine histogram
@app.callback(
    dash.dependencies.Output('graph2', 'figure'),
    [dash.dependencies.Input('dropdown', 'value'),
     dash.dependencies.Input('distribution', 'value'), 
     dash.dependencies.Input('dropdown2', 'value')])
def display_graph(cytokine, distribution, bins_):
    fig = px.histogram(
        df_, x = cytokine, color="Treatment Conditions",
        marginal=distribution,
        hover_data=df_.columns, nbins = bins_,  
        #title = cytokine + " Histogram", 
        color_discrete_map = color_discrete_map)
    fig.update_layout(title_text=cytokine + " Histogram", title_x=0.5)
    fig.update_layout(plot_bgcolor='rgb(255,255,255)')
    return fig
#callback - individual cytokine density plot
@app.callback(
    dash.dependencies.Output('graph3', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])

def dist_plot_graph(cytokine):
    #this ensures that colors remain in the same order for all of the graphs
    color_discrete_map1 = color_discrete_map.copy()
    df = df_[["Treatment Conditions", cytokine]]
    hist_data  = []
    group_labels = []
    for i in df["Treatment Conditions"].unique().tolist():
        sub_vals  = df.loc[df["Treatment Conditions"] == i, cytokine]
        #this condition will bypass 0 matrices errors for density plot
        if sub_vals.sum() == 0:
            del color_discrete_map1[i]
        else:
            group_labels.append(str(i))
            hist_data.append(list(sub_vals))
    new_colors=list(color_discrete_map1.values())
    fig = ff.create_distplot(hist_data, group_labels, colors = new_colors, show_hist = False, show_rug=False)
    fig.update_layout(title_text=cytokine + " Density Plot", title_x=0.5)
    fig.update_layout(plot_bgcolor='rgb(255,255,255)')
    return(fig)

#callback Non-zero Proportion function - known as "cytokine secreting"
@app.callback(
    [dash.dependencies.Output('stats_nz', 'children'),
    dash.dependencies.Output('p_val_nz', 'children')],
    [dash.dependencies.Input('dropdown', 'value'),
     dash.dependencies.Input('option_1_stat', 'value'), 
     dash.dependencies.Input('option_2_stat', 'value')])

def nz_prop_test(cytokine, match1, match2):
    #separated conditions and takes the sum of the non-zero values
    #example: 20/50 in an array are non-zero.
    #this is compared for two conditions
    #Z statistic and P-value are outputted to the user
    comp_1 = df_.loc[df_['Treatment Conditions'] == match1, cytokine]
    non_zero_sum_1 = (comp_1 != 0).sum()
    len_t1 = len(comp_1)
    comp_2 = df_.loc[df_['Treatment Conditions'] == match2, cytokine]
    non_zero_sum_2 = (comp_2 != 0).sum()
    len_t2 = len(comp_2)
    successes = np.array([non_zero_sum_1, non_zero_sum_2])
    samples = np.array([len_t1, len_t2])
    stat_1, p_value_1 = proportions_ztest(count=successes, nobs=samples,  alternative='two-sided')
    stat_ = '{0:.2f}'.format(stat_1)
    stat_ = "Non-Zero Proportion Z Statistic: " + str(stat_)
    p_value_ = '{0:.2f}'.format(p_value_1)
    p_value_ = "Non-Zero Proportion P-Value: " + str(p_value_)
    return(stat_, p_value_)
#callback statistics
@app.callback(
    [dash.dependencies.Output('stats_ks', 'children'),
    dash.dependencies.Output('p_val_ks', 'children')],
    [dash.dependencies.Input('dropdown', 'value'),
     dash.dependencies.Input('option_1_stat', 'value'), 
     dash.dependencies.Input('option_2_stat', 'value')])

def all_prop_test(cytokine, match1, match2):
    comp_1 = df_.loc[df_['Treatment Conditions'] == match1, cytokine].to_list()
    comp_2 = df_.loc[df_['Treatment Conditions'] == match2, cytokine].to_list()
    stat_1, p_value_1 = ks_2samp(comp_1, comp_2)
    stat_ = '{0:.2f}'.format(stat_1)
    stat_ = "KS-Test Proportion Z Statistic: " + str(stat_)
    p_value_ = '{0:.2f}'.format(p_value_1)
    p_value_ = "KS-Test Proportion P-Value: " + str(p_value_)
    return(stat_, p_value_)

@app.callback(
    [dash.dependencies.Output('value_sum', 'children'),
    dash.dependencies.Output('zero_sum', 'children'),
    dash.dependencies.Output('mean_std_all', 'children'),
    dash.dependencies.Output('min_max_all', 'children'),
    dash.dependencies.Output('mean_std_nz', 'children'),
    dash.dependencies.Output('min_max_nz', 'children')],
    [dash.dependencies.Input('dropdown', 'value'),
     dash.dependencies.Input('dropdown_stat', 'value')])

def cyto_stats(cytokine, condition):
    if condition == "All":
        comp_1 = df_[cytokine]
    else:
        comp_1 = df_.loc[df_['Treatment Conditions'] == condition, cytokine]
    #Across all samples and Treatment Conditions
    #Number of cells for cytokine with non-zero values
    value_sum_1 = (comp_1 != 0).sum()
    value_sum = '{0:.0f}'.format(value_sum_1)
    value_sum = "Number of Cells With Values: " + str(value_sum)
    #Number of cells for cytokine with zero values
    zero_sum_1 = (comp_1 == 0).sum()
    zero_sum = '{0:.0f}'.format(zero_sum_1)
    zero_sum = "Number of Cells with No Values: " + str(zero_sum)
    #mean of all cells across cytokine
    mean_df_all_1 = comp_1.mean()
    mean_df_all = '{0:.2f}'.format(mean_df_all_1)
    std_df_all_1 = comp_1.std()
    std_df_all = '{0:.2f}'.format(std_df_all_1)
    mean_std_all = "Mean and Standard Deviation Across All Cells: " + str(mean_df_all)+ " and " + str(std_df_all)
    min_df_all_1 = comp_1.min()
    min_df_all = '{0:.2f}'.format( min_df_all_1)
    max_df_all_1 = comp_1.max()
    max_df_all = '{0:.2f}'.format( max_df_all_1)
    min_max_all = "Minimum and Maximum Values Across All Cells: " + str(min_df_all)+ " and " + str(max_df_all)
    #stats of Non-zero cells across cytokine
    mean_df_nz_1 = comp_1[comp_1!= 0].mean()
    mean_df_nz = '{0:.2f}'.format(mean_df_nz_1)
    std_df_nz_1 = comp_1[comp_1!= 0].std()
    std_df_nz = '{0:.2f}'.format(std_df_nz_1)
    min_df_nz_1 = comp_1[comp_1!= 0].min()
    min_df_nz = '{0:.2f}'.format(min_df_nz_1)
    max_df_nz_1 = comp_1[comp_1!= 0].max()
    max_df_nz = '{0:.2f}'.format(max_df_nz_1)
    mean_std_nz = "Mean and Standard Deviation Across All Non-Zero Cells: " + str(mean_df_nz)+ " and " + str(std_df_nz)
    min_max_nz = "Minimum and Maximum Values Across All Non-Zero Cells: " + str(min_df_nz)+ " and " + str(max_df_nz)
    return(value_sum, zero_sum, mean_std_all, min_max_all, mean_std_nz, min_max_nz)

app.run_server(debug=True)