import dash
dash.register_page(__name__, title = 'Non-Zero Proportions')
from dash import dcc, html, Input, Output, callback
import plotly.express as px
from dash import no_update
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State


centerStyle = {'textAlign': 'center'}

layout = html.Div(
    [   html.H2("Percent Cytokines Secreted Across Treatment Conditions"),
        html.P("Percent Cytokine Secreted:calculated by taking non-zero proportions for each treatment condition across each cytokine."),
        dcc.Graph(id="bar_plot_all"),
        html.Div(html.P(id = 'bar_all_information'))
    ], style = centerStyle
)

#callback: bar graph of all nz proportions
@callback(Output('bar_plot_all', 'figure'),
            Input('analysis-button','n_clicks'),
            Input('cyto_list', 'data'),
            State ('stored-data-reordered', 'data'),
            State ('color_discrete_map', 'data'))

#Non-zero Proportions Graph for All Cytokines
#this produces a NZ Proportion dataframe
def non_zero_prop_bar_all(n, cyto_list, df, color_discrete_map):
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
        return (bar_ALL)
