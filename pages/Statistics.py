import dash
dash.register_page(__name__, title = 'Distribution and Statistics')
from dash import dcc, html, Input, Output, callback
import plotly.express as px
from dash import no_update
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff
from statsmodels.stats.proportion import proportions_ztest
from scipy.stats import ks_2samp
import numpy as np
from dash.exceptions import PreventUpdate

#bins used for the histogram 
bins = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

centerStyle = {'textAlign': 'center'}

layout = html.Div(
    [   
        html.H2("Percent Cytokines Secreted Across Treatment Conditions", style = centerStyle),
        html.P("Percent Cytokine Secreted: calculated by taking non-zero proportions for each treatment condition across each cytokine.", style =centerStyle),
        dcc.Graph(id="bar_plot_all"),
        dcc.Store(id = 'nz_table'),
        dbc.Row([
        dbc.Col(html.Div([
        html.H4("Cytokine Statistics for Individual Cytokine", style=centerStyle),
        dcc.RadioItems(
        id="stat_options",
        value="All",
        inline=True, inputStyle={"margin-right": "5px", "margin-left": "5px"}, 
        style=centerStyle),
        html.Div(html.H4(id='value_sum')),
        html.Div(html.H4(id='zero_sum')),
        html.Div(html.H4(id='mean_std_all')),
        html.Div(html.H4(id='min_max_all')),
        html.Div(html.H4(id='mean_std_nz')),
        html.Div(html.H4(id='min_max_nz')),
        ]), width={"size": 4}),

        dbc.Col(html.Div([
        html.H4("Statistical Tests for Differences in Cytokine Secretion", style={'textAlign': 'center'}),
        html.H4(dcc.Markdown('''_Select Condition 1:_
        '''), style=centerStyle),
        dcc.RadioItems(id="option_1_stat", inline=True, inputStyle={"margin-right": "5px", "margin-left": "5px"}, 
        style=centerStyle),
        html.H4(dcc.Markdown('''_Select Condition 2:_
        '''), style=centerStyle),
        dcc.RadioItems(id="option_2_stat", inline=True, inputStyle={"margin-right": "5px", "margin-left": "5px"}, 
        style=centerStyle),
        # NZ Proportion Stats Call
        html.H4(dcc.Markdown('''**Percent Cytokines Secreting - Proportion Test**
        '''), style=centerStyle),
        html.P('The Non-Zero Proportion Test determines whether the non-zero proportion of two samples are significantly different from each other.', style =centerStyle),
        html.Div(id='stats_nz', style=centerStyle),
        html.Div( id='p_val_nz', style=centerStyle),
        #KS Test
        html.H4(dcc.Markdown('''**Kolmogorov-Smirnov Test**
        '''), style=centerStyle),
        html.P("The Kolmogorov-Smirnov Test is a non-parametric test that determines if two samples are significantly different from each other.", style =centerStyle),
        html.Div(id='stats_ks' , style=centerStyle),
        html.Div( id='p_val_ks', style=centerStyle)
        ]), width={"size": 4}),

        dbc.Col(html.Div([
            dcc.Graph(id = 'bar_individual'),
            html.P("Note: if you would like to view individual cytokine expression of a different cytokine, repeat step 5."),

        ]), width={"size": 4})


    ]),
        html.H2("Individual Cytokine Distribution", style = centerStyle),
        dbc.Row(
            [dbc.Col(html.Div([
        dcc.Graph(id="graph_hist"),
        html.P("Select Bin Size", style={'textAlign': 'center'}),
        dcc.RadioItems(
        id="bins",
        options=bins,
        value=20,
        style={'textAlign': 'center'}, inputStyle={"margin-right": "5px", "margin-left": "5px"}),
        html.P("Select Box Plot, Violin Plot or Rug Plot:", style={'textAlign': 'center'}),
        dcc.RadioItems(
        id='distribution',
        options=[{'label':'Box Plot', 'value':'box'}, {'label':'Violin Plot', 'value':'violin'}, 
                 {'label':'Rug Plot','value': 'rug'}],
        value='box', inline=True, inputStyle={"margin-right": "5px", "margin-left": "5px"}, 
            style=centerStyle)])),
        dbc.Col(html.Div([
        dcc.Graph(id="graph_dens"),
        html.P("Density plots allow for the visualization of the distribution of a numeric variables for one or more groups.")
        ]))
        ], style = centerStyle),
    
    ]
)

#callback for all statistics options
@callback(
    Output('stat_options', 'options'),
    Input('analysis-button','n_clicks'),
    State('ordered_list', 'value'))
def histdendro_all_callback(n, selected_cytokine):
    try: 
        if n is None: 
            return no_update
        else:
            return ["All"] +selected_cytokine
    except:
         no_update

#callback for treatment conditions
@callback(
    Output('option_1_stat', 'options'),
    Input('analysis-button','n_clicks'),
    State('ordered_list', 'value'))
def treatment_all_callback1(n, selected_cytokine): 
    try:
        if n is None: 
            return no_update
        else:
            return selected_cytokine
    except:
        return no_update


#callback for treatment conditions
@callback(
    Output('option_2_stat', 'options'),
    Input('analysis-button','n_clicks'),
    State('ordered_list', 'value'))
def treatment_all_callback2(n, selected_cytokine): 
    try:
        if n is None: 
            return no_update
        else:
            return selected_cytokine
    except:
        return no_update

@callback(Output('value_sum', 'children'),
            Output('zero_sum', 'children'),
            Output('mean_std_all', 'children'),
            Output('min_max_all', 'children'),
            Output('mean_std_nz', 'children'),
            Output('min_max_nz', 'children'),
            Input('indiv-cyto-button','n_clicks'),
            State('indiv_cyto_dropdown', 'value'),
            Input('stat_options', 'value'),
            State ('stored-data-reordered', 'data'))

def cyto_stats(n, cytokine, condition, df):
    if n is None: 
        return no_update
    else:
        df =pd.DataFrame(df)
        if condition == "All":
            comp_1 = df[cytokine]
        else:
            comp_1 = df.loc[df['Treatment Conditions'] == condition, cytokine]
        #Across all samples and Treatment Conditions
        #Number of cells for cytokine with non-zero values
        value_sum_1 = (comp_1 != 0).sum()
        value_sum = f"{value_sum_1:.4e}"
        value_sum = "Number of Cells with Values: " + str(value_sum)
        #Number of cells for cytokine with zero values
        zero_sum_1 = (comp_1 == 0).sum()
        zero_sum = f"{zero_sum_1:.4e}"
        zero_sum = "Number of Cells with No Values: " + str(zero_sum)
        #mean of all cells across cytokine
        mean_df_all_1 = comp_1.mean()
        mean_df_all = f"{mean_df_all_1:.4e}"
        std_df_all_1 = comp_1.std()
        std_df_all = f"{std_df_all_1:.4e}"
        mean_std_all = "Mean and Standard Deviation Across All Cells: " + str(mean_df_all)+ " and " + str(std_df_all)
        min_df_all_1 = comp_1.min()
        min_df_all = f"{min_df_all_1:.4e}"
        max_df_all_1 = comp_1.max()
        max_df_all = f"{max_df_all_1:.4e}"
        min_max_all = "Minimum and Maximum Values Across All Cells: " + str(min_df_all)+ " and " + str(max_df_all)
        #stats of Non-zero cells across cytokine
        mean_df_nz_1 = comp_1[comp_1!= 0].mean()
        mean_df_nz = f"{mean_df_nz_1:.4e}"
        std_df_nz_1 = comp_1[comp_1!= 0].std()
        std_df_nz = f"{std_df_nz_1:.4e}"
        min_df_nz_1 = comp_1[comp_1!= 0].min()
        min_df_nz = f"{min_df_nz_1:.4e}"
        max_df_nz_1 = comp_1[comp_1!= 0].max()
        max_df_nz =  f"{max_df_nz_1:.4e}"
        mean_std_nz = "Mean and Standard Deviation Across All Non-Zero Cells: " + str(mean_df_nz)+ " and " + str(std_df_nz)
        min_max_nz = "Minimum and Maximum Values Across All Non-Zero Cells: " + str(min_df_nz)+ " and " + str(max_df_nz)
        return(value_sum, zero_sum, mean_std_all, min_max_all, mean_std_nz, min_max_nz)
    
#callback Non-zero Proportion function - known as "cytokines secreting"
@callback(
    Output('stats_nz', 'children'),
    Output('p_val_nz', 'children'),
    Input('indiv-cyto-button','n_clicks'),
    State('indiv_cyto_dropdown', 'value'),
    Input('option_1_stat', 'value'), 
    Input('option_2_stat', 'value'),
    State ('stored-data-reordered', 'data'))

def nz_prop_test(n, cytokine, match1, match2, df):
    if n is None: 
        return no_update
    else:
        if (match1 is None) or (match2 is None):
            return no_update
        else:
            df =pd.DataFrame(df)
            #separated conditions and takes the sum of the non-zero values
            #example: 20/50 in an array are non-zero.
            #this is compared for two conditions
            #Z statistic and P-value are outputted to the user
            comp_1 = df.loc[df['Treatment Conditions'] == match1, cytokine]
            non_zero_sum_1 = (comp_1 != 0).sum()
            len_t1 = len(comp_1)
            comp_2 = df.loc[df['Treatment Conditions'] == match2, cytokine]
            non_zero_sum_2 = (comp_2 != 0).sum()
            len_t2 = len(comp_2)
            successes = np.array([non_zero_sum_1, non_zero_sum_2])
            samples = np.array([len_t1, len_t2])
            stat_1, p_value_1 = proportions_ztest(count=successes, nobs=samples,  alternative='two-sided')
            stat_ = f"{stat_1:.4e}"
            stat_ = "Non-Zero Proportion Z Statistic: " + str(stat_)
            p_value_ = f"{p_value_1:.4e}"
            p_value_ = "Non-Zero Proportion P-Value: " + str(p_value_)
            return(stat_, p_value_)

#callback Non-zero Proportion function - known as "cytokines secreting"
@callback(
    Output('stats_ks', 'children'),
    Output('p_val_ks', 'children'),
    Input('indiv-cyto-button','n_clicks'),
    State('indiv_cyto_dropdown', 'value'),
    Input('option_1_stat', 'value'), 
    Input('option_2_stat', 'value'),
    State ('stored-data-reordered', 'data'))

def all_prop_test(n, cytokine, match1, match2, df):
    if n is None: 
        return no_update
    else:
        if (match1 is None) or (match2 is None):
            return no_update
        else:
            df =pd.DataFrame(df)
            comp_1 = df.loc[df['Treatment Conditions'] == match1, cytokine].to_list()
            comp_2 = df.loc[df['Treatment Conditions'] == match2, cytokine].to_list()
            stat_1, p_value_1 = ks_2samp(comp_1, comp_2)
            stat_ = f"{stat_1:.4e}"
            stat_ = "KS-Test Proportion Z Statistic: " + str(stat_)
            p_value_ = f"{p_value_1:.4e}"
            p_value_ = "KS-Test Proportion P-Value: " + str(p_value_)
            return(stat_, p_value_)

#callback: bar graph of all nz proportions
@callback(Output('bar_plot_all', 'figure'),
            Output('nz_table', 'data'),
            Input('analysis-button','n_clicks'),
            Input('cyto_list', 'data'),
            State ('stored-data-reordered', 'data'),
            State ('color_discrete_map', 'data'))

#Non-zero Proportions Graph for All Cytokines
#this produces a NZ Proportion dataframe
def non_zero_prop_bar_all(n, cyto_list, df, color_discrete_map):
    try:
        if n is None: 
            return no_update
        else:
            #insertion adds the subtype "Treatment Conditions" to front of the list.
            #this is used to create the NZ Proportion table
            edit_cyto_list = cyto_list.copy()
            edit_cyto_list.insert(0, "Treatment Conditions")
            df = pd.DataFrame(df)
            df_1 = df[edit_cyto_list] 
            df_values = pd.DataFrame(cyto_list, columns = ["Cytokines"] )
            for i in df_1["Treatment Conditions"].unique().tolist():
                list_sub = []
                sub_df = df_1.loc[df_1["Treatment Conditions"] == i]
                sub_df.pop("Treatment Conditions")
                for column in sub_df:
                    new_val = ((sub_df[column] != 0).sum())/len(sub_df[column])
                    list_sub.append(new_val)
                df_values[str(i)] = list_sub
            ###this reformats the NZ Proportions dataframe, so that the bar graph can be produced
            df_edit =pd.melt(df_values, id_vars=["Cytokines"],var_name='Treatment Conditions', 
                            value_name = 'Percent Cytokines Secreting')
            ###Bar plot for all cytokines
            bar_ALL = px.bar(df_edit, x="Cytokines", color="Treatment Conditions",
                y='Percent Cytokines Secreting',
                barmode='group', color_discrete_map = color_discrete_map,
                height=500)
            bar_ALL.update_layout(title_text= 'Percent Cytokine Secreting', title_x = 0.5)
            bar_ALL.update_layout(plot_bgcolor='rgb(255,255,255)')
            return (bar_ALL, df_edit.to_dict('records'))
    except:
        return no_update

#callback for nz propprtion individual cytokine barplot
@callback(Output('bar_individual', 'figure'),
            Input('indiv-cyto-button','n_clicks'),
            State('indiv_cyto_dropdown', 'value'),
            Input ('nz_table', 'data'), 
            State ('color_discrete_map', 'data'))

def update_bar_chart(n, cytokine, df, color_discrete_map):
    if n is None: 
        return no_update
    else:
        df =pd.DataFrame(df)
        mask = df["Cytokines"] == cytokine
        fig = px.bar(df[mask], x="Treatment Conditions", y="Percent Cytokines Secreting", 
            color="Treatment Conditions", color_discrete_map = color_discrete_map, barmode="group",
            #title = cytokine + " Non-Zero Proportions", 
            text_auto = True)
        fig.update_layout(title_text=cytokine + " Percent Cytokines Secreting", title_x=0.5)
        fig.update_layout(plot_bgcolor='rgb(255,255,255)')
        return fig

#callback for histogram
@callback(Output('graph_hist', 'figure'),
            Input('indiv-cyto-button','n_clicks'),
            State('indiv_cyto_dropdown', 'value'), 
            Input ('stored-data-reordered', 'data'), 
            State ('color_discrete_map', 'data'),
            Input ('distribution', 'value'), 
            Input ('bins', 'value'))

def graph_histogram(n, cytokine, df, color_discrete_map, distribution, bins):
    if n is None:
        return no_update
    else:
        try:
            df = pd.DataFrame(df)
            fig = px.histogram(df, x = cytokine, color="Treatment Conditions",marginal=distribution,
                            hover_data=df.columns, nbins = bins,  title = cytokine + " Histogram", 
                            color_discrete_map = color_discrete_map)
            fig.update_layout(title_text=cytokine + " Histogram", title_x=0.5)
            fig.update_layout(plot_bgcolor='rgb(255,255,255)')
            return fig
        except: 
            df = pd.DataFrame(df)
            fig = px.histogram(df, x = cytokine, color="Treatment Conditions",marginal="box",
                            hover_data=df.columns, nbins = 20,  title = cytokine + " Histogram", 
                            color_discrete_map = color_discrete_map)
            fig.update_layout(title_text=cytokine + " Histogram", title_x=0.5)
            fig.update_layout(plot_bgcolor='rgb(255,255,255)')
            return fig
        

#callback for density plot
@callback(Output('graph_dens', 'figure'),
            Input('indiv-cyto-button','n_clicks'),
            State('indiv_cyto_dropdown', 'value'),
            Input ('stored-data-reordered', 'data'), 
            State ('color_discrete_map', 'data'))

def dist_plot_graph(n, cytokine, df, color_discrete_map):
    if n is None: 
        raise PreventUpdate
    else:
        df = pd.DataFrame(df)
        #this ensures that colors remain in the same order for all of the graphs
        color_discrete_map1 = color_discrete_map.copy()
        df = df[["Treatment Conditions", cytokine]]
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