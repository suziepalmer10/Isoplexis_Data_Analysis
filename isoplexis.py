import dash
import dash_labs as dl 
import dash_bootstrap_components as dbc 
import base64
import datetime
import io
from dash.dependencies import Input, Output, State
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
from dash import no_update


secretome_selection = ['Mouse Adaptive Immune', 'Human Adaptive Immune', 'NHP Adaptive Immune', 
'Human Inflammation', 'Human Innate Immune']

#this is the original description list
description_list = ["Donor", "Cell Subset", "Stimulation"]

centerStyle = {'textAlign': 'center'}


app = dash.Dash(
    __name__, plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True
)

#code for navigation bar
navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["title"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="Data Analysis Options",
    ),
    brand="Isoplexis Data Analysis",
    color="primary",
    dark=True,
    className="mb-2",
)
#code for user file upload
userInput = dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    )

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            #this column creates a new column which combines all of the descriptions
            df['Treatment Conditions'] = df[description_list].apply(
                lambda x: ' '.join(x.dropna().astype(str)),
                axis=1)
            #this list will be allow the user to plot graphs in desired order
            df_labels_un = list(df['Treatment Conditions'].unique())
            #heatmap index positions maintained for cells
            num_cells = range(1, len(df)+1)
            df['Permanent Index'] = num_cells
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            df['Treatment Conditions'] = df[description_list].apply(
                lambda x: ' '.join(x.dropna().astype(str)),
                axis=1)
            #this list will be allow the user to plot graphs in desired order
            df_labels_un = list(df['Treatment Conditions'].unique())
            #heatmap index positions maintained for cells
            num_cells = range(1, len(df)+1)
            df['Permanent Index'] = num_cells
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H4('Uploaded File Information: ', style=centerStyle),
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        #this stores the data to be used for future callbacks
        dcc.Store(id='stored-data', data=df.to_dict('records')),
        html.H4('Step 2: Select the Assay used for the Isoplexis Analysis: ', style =  {'textAlign': 'left'}),
        html.P("This will determine the cytokines read for the assay.", style =  {'textAlign': 'left'}),
        dcc.RadioItems(
            id="secretome_type",
            options=secretome_selection,
            value= "Mouse Adaptive Immune",
            inline=True, inputStyle={"margin-right": "5px", "margin-left": "5px"}, 
            style=centerStyle),
        html.H4('Step 3: Select the Conditions that will be Analyzed:', style = {'textAlign': 'left'}),
        html.P("Note: The order (left to right) of items selected will be the same order for the graphs. ", style =  {'textAlign': 'left'}),
        # list for user to reorder data
        dcc.Dropdown(
            id="ordered_list",
            options=df_labels_un,
            multi = True), 
        html.Button(id="submit-button", children="Reorder Data"),
        html.H4('Step 4: Select the Button Below to Analyze Isoplexis Data:', style = {'textAlign': 'left'}),
        html.Div(html.Button(id="analysis-button", children="Analyze Isoplexis Data"), style = {'textAlign': 'left'}),
        html.P('Note: If you decide to reorder your data after selecting the analysis button, you will need to repeat steps 3 and 4 again.',
        style = {'textAlign': 'left'}),
        html.H4("Step 5: To view individual cytokine analysis, select a cytokine from this list below.", style={'textAlign': 'left'}),
        html.P("Note: each analysis page has a section to view individual cytokines. If the cytokine has no value, it will not appear on this list.", style={'textAlign': 'left'}),
        html.Div(dcc.Dropdown(
        id='indiv_cyto_dropdown',
        placeholder="Select a cytokine for individual cytokine analysis",
        clearable=False),
        style={"width": "50%"}),

        html.Div(html.Button(id="indiv-cyto-button", children="Analyze Individual Cytokine"), style = {'textAlign': 'left'}),
        html.P("In order to change individual cytokine, select desired cytokine from the dropdown menu and click 'Analyze Individual Cytokine' button again.", style = {'textAlign': 'left'})

    ])

app.layout = dbc.Container(
    [navbar, 
    #header 
    html.H1('Isoplexis Data Analysis', style = centerStyle),
    html.H2('Suzette Palmer', style = centerStyle),
    html.H3('Zhan and Koh Labs', style = centerStyle),
    html.H4('University of Texas Southwestern Medical Center', style =centerStyle),
    #user file input
    html.H4('Step 1: Upload Isoplexis Data Analysis File:'),
    html.P('Note: Formats allowed are comma separated values (csv) or excel (xls).'),
    userInput, 
    #output file information
    html.Div(id='output-data-upload', style =centerStyle),
    dcc.Store(id = 'cyto_list'),
    dcc.Store(id = 'stored-data-reordered'),
    dcc.Store(id='color_discrete_map'),
    dl.plugins.page_container], fluid=True )

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@app.callback(Output('cyto_list', 'data'),
            Input('secretome_type', 'value'))
def cyto_secretion_list(val):
    if val is None:
        raise PreventUpdate

    else:
        if val == "Mouse Adaptive Immune":
            cyto_list = ['BCA-1', 'CCL-11', 'FAS', 'GM-CSF', 'Granzyme B', 
                    'IFN-g', 'IL-10', 'IL-12p70', 'IL-13', 'IL-15', 'IL-17A', 
                    'IL-18', 'IL-1b', 'IL-2', 'IL-21', 'IL-27', 'IL-4', 
                    'IL-5', 'IL-6', 'IL-7', 'IP-10', 'KC', 'MCP-1', 'MIP-1a', 
                    'RANTES', 'sCD137', 'TGF-b', 'TNF-a']
        elif val  == 'Human Adaptive Immune':
            cyto_list = ['Granzyme B', 'IFN-g', 'MIP-1a', 'Perforin', 'TNF-a',
                    'TNF-b', 'GM-CSF', 'IL-2', 'IL-5', 'IL-7', 'IL-8', 'IL-9', 'IL-12', 'IL-15', 
                    'IL-21', 'CCL-11', 'IP-10', 'MIP-1b', 'RANTES', 'IL-4', 'IL-10', 'IL-13',
                    'IL-22', 'TGF-b1', 'sCD137', 'sCD40L', 'IL-1b', 'IL-6', 'IL-17a', 'IL-17f',
                    'MCP-1', 'MCP-4']
        elif val == 'NHP Adaptive Immune':
            cyto_list = ['TNF-a', 'MCP-1', 'IL-2', 'IL-4', 'MIP-1b', 'IL-6', 'IL-8',
                    'IL-1b', 'RANTES', 'IFN-g', 'IP-10', 'MIP-1a', 'MIF', 'GM-CSF']
        elif val == 'Human Inflammation':
            cyto_list = ["GM-CSF", 'IFN-g', 'IL-2', 'IL-12', 'TNF-a', 'TNF-b', 'IL-4',
                    'IL-5', 'IL-7', 'IL-9', 'IL-13', 'CCL11', 'IL-8', 'IP-10', 'MCP-1', 'MCP-4', 'MIP-1a',
                    'MIP-1b', 'RANTES', 'IL-10', 'IL-15', 'IL-22', 'TGF-b1', 'IL-1b', 'IL-6', 'IL-17a', 
                    'IL-17f', 'IL-21', 'Granzyme B', 'Perforin', 'sCD40L', 'sCD137']
        else:
            cyto_list = ['IFN-g', 'MIP-1a', 'TNF-a', 'TNF-b', 'Stimulatory', 'GM-CSF', 
                    'IL-8', 'IL-9', 'IL-15', 'IL-18', 'TGF-a', 'IL-5', 'CCL11', 'IP-10', 'MIP-1b', 
                    'RANTES', 'BCA-1', 'IL-10', 'IL-13', 'IL-22', 'sCD40L', 'IL-1b', 'IL-6', 
                    'IL-12-p40', 'IL-12', 'IL-17a', 'IL-17f', 'MCP-1', 'MCP-4', 'MIF', 'EGF',
                    'PDGF-BB', 'VEGF']
        return cyto_list


@app.callback(Output('stored-data-reordered', 'data'),
            Input('submit-button','n_clicks'),
            State('ordered_list', 'value'),
            Input('stored-data','data'))
def permutationToPlot (n, selected_permutation, data):
    if n is None:
        data = pd.DataFrame(data)
        return data.to_dict('records')
    else:
        data = pd.DataFrame(data)
        #this function reorders the dataframe so user can select which order to plot
        count = 0;
        for i in selected_permutation:
            if count == 0:
                new_data = data[data["Treatment Conditions"] == i]
                count = count + 1
            else:
                df_to_append = data[data["Treatment Conditions"] == i]
                new_data = pd.concat([new_data, df_to_append])
                count = count + 1
        
        return new_data.to_dict('records')

#this makes sure the color schemes for the bar plots, density and histogram are consistent
@app.callback(Output('color_discrete_map', 'data'),
            Input('submit-button','n_clicks'),
            State('ordered_list', 'value'))

def discrete_color(n, selected_permutation):
    if n is None:
        return no_update
    else: 
        #this makes sure colors are the same for bar plots, density and histogram
        #better separation of colors - uses the thermal palette
        colors = ['rgb(3, 35, 51)', 
        #'rgb(13, 48, 100)', 
        'rgb(53, 50, 155)', 
        #'rgb(93, 62, 153)', 
        'rgb(126, 77, 143)', 
        #'rgb(158, 89, 135)', 
        'rgb(193, 100, 121)', 
        #'rgb(225, 113, 97)', 
        'rgb(246, 139, 69)', 
        #'rgb(251, 173, 60)', 
        'rgb(246, 211, 70)', 
        #'rgb(231, 250, 90)'
        ]
        colors_for_plot = colors[:len(selected_permutation)]
        color_discrete_map = {selected_permutation[i]: colors_for_plot[i] for i in range(len(selected_permutation))}
        return color_discrete_map

@app.callback(
    Output('indiv_cyto_dropdown', 'options'),
    Input('submit-button','n_clicks'),
    Input('indiv-cyto-button','n_clicks'),
    State('cyto_list', 'data'),
    State('ordered_list', 'value'),
    State('stored-data-reordered', 'data'))

def individual_cyto_callback(n, m, cyto_list, selected_cytokine, df):
    if (n is None) and (m is None): 
        return no_update

    else: 
        df = pd.DataFrame(df)
        ##create an edited cytokine list for dropdown 
        ##columns with no values will be removed
        edit_cyto_list = []
        for i in cyto_list:
            if df[i].sum() == 0:
                continue
            else: 
                edit_cyto_list.append(i)
        ###create dictionary for dynamic callbacks for dendrogram and heatmap
        heatmap_dictionary = []
        for cytokine in edit_cyto_list:
            small_list = ["All"]
            for i in selected_cytokine: 
                sub_vals  = df.loc[df["Treatment Conditions"] == i, cytokine]
                if sub_vals.sum() != 0:
                    #not sure if either or both is needed for this 
                    small_list.append(i)
            heatmap_dictionary.append(small_list)
        # using dictionary comprehension to convert lists to dictionary
        #main dictionary used for the callbacks. 
        cytokine_dictionary = {edit_cyto_list[i]: heatmap_dictionary[i] for i in range(len(edit_cyto_list))}
        options=[{'label': k, 'value': k} for k in cytokine_dictionary.keys()]
        return options


if __name__ == "__main__":
    app.run_server(debug=True)


