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


secretome_selection = ['Mouse Adaptive Immune', 'Human Adaptive Immune', 'Non-Human Primate Adaptive Immune',
                       'Human Inflammation', 'Human Innate Immune']
# this is the original description list
description_list = ["Donor", "Cell Subset", "Stimulation"]

mouse_adaptive_immune = {'BCA-1': 'Chemoattractive',
                         'CCL-11': 'Chemoattractive',
                         'FAS': 'Regulatory',
                         'GM-CSF': 'Stimulatory',
                         'Granzyme B': 'Effector',
                         'IFN-g': 'Effector',
                         'IL-10': 'Regulatory',
                         'IL-12p70': 'Stimulatory',
                         'IL-13': 'Regulatory',
                         'IL-15': 'Stimulatory',
                         'IL-17A': 'Inflammatory',
                         'IL-18': 'Stimulatory',
                         'IL-1b': 'Inflammatory',
                         'IL-2': 'Stimulatory',
                         'IL-21': 'Stimulatory',
                         'IL-27': 'Regulatory',
                         'IL-4': 'Regulatory',
                         'IL-5': 'Stimulatory',
                         'IL-6': 'Inflammatory',
                         'IL-7': 'Stimulatory',
                         'IP-10': 'Chemoattractive',
                         'KC': 'Chemoattractive',
                         'MCP-1': 'Inflammatory',
                         'MIP-1a': 'Effector',
                         'RANTES': 'Chemoattractive',
                         'sCD137': 'Stimulatory',
                         'TGF-b': 'Regulatory',
                         'TNF-a': 'Effector'}

human_adaptive_immune = {'CCL-11': 'Chemoattractive',
                         'GM-CSF': 'Stimulatory',
                         'Granzyme B': 'Effector',
                         'IFN-g': 'Effector',
                         'IL-10': 'Regulatory',
                         'IL-12': 'Stimulatory',
                         'IL-13': 'Regulatory',
                         'IL-15': 'Stimulatory',
                         'IL-17a': 'Inflammatory',
                         'IL-17f': 'Inflammatory',
                         'IL-1b': 'Inflammatory',
                         'IL-2': 'Stimulatory',
                         'IL-21': 'Stimulatory',
                         'IL-22': 'Regulatory',
                         'IL-4': 'Regulatory',
                         'IL-5': 'Stimulatory',
                         'IL-6': 'Inflammatory',
                         'IL-7': 'Stimulatory',
                         'IL-8': 'Stimulatory',
                         'IL-9': 'Stimulatory',
                         'IP-10': 'Chemoattractive',
                         'MCP-1': 'Inflammatory',
                         'MCP-4': 'Inflammatory',
                         'MIP-1a': 'Effector',
                         'MIP-1b': 'Chemoattractive',
                         'Perforin': 'Effector',
                         'RANTES': 'Chemoattractive',
                         'TGF-b1': 'Regulatory',
                         'TNF-a': 'Effector',
                         'TNF-b': 'Effector',
                         'sCD137': 'Regulatory',
                         'sCD40L': 'Regulatory'}

nhp_adaptive_immune = {'GM-CSF': 'Stimulatory',
                       'IFN-g': 'Effector',
                       'IL-1b': 'Inflammatory',
                       'IL-2': 'Stimulatory',
                       'IL-4': 'Regulatory',
                       'IL-6': 'Inflammatory',
                       'IL-8': 'Stimulatory',
                       'IP-10': 'Chemoattractive',
                       'MCP-1': 'Inflammatory',
                       'MIF': 'Inflammatory',
                       'MIP-1a': 'Effector',
                       'MIP-1b': 'Chemoattractive',
                       'RANTES': 'Chemoattractive',
                       'TNF-a': 'Effector'}

human_inflammation = {'CCL11': 'Chemoattractive',
                      'GM-CSF': 'TH1 Pro Inflammatory',
                      'Granzyme B': 'Cytolytic',
                      'IFN-g': 'TH1 Pro Inflammatory',
                      'IL-10': 'Regulatory',
                      'IL-12': 'TH1 Pro Inflammatory',
                      'IL-13': 'TH2 Pro Inflammatory',
                      'IL-15': 'Regulatory',
                      'IL-17a': 'TH17 Pro Inflammatory',
                      'IL-17f': 'TH17 Pro Inflammatory',
                      'IL-1b': 'TH17 Pro Inflammatory',
                      'IL-2': 'TH1 Pro Inflammatory',
                      'IL-21': 'TH17 Pro Inflammatory',
                      'IL-22': 'Regulatory',
                      'IL-4': 'TH2 Pro Inflammatory',
                      'IL-5': 'TH2 Pro Inflammatory',
                      'IL-6': 'TH17 Pro Inflammatory',
                      'IL-7': 'TH2 Pro Inflammatory',
                      'IL-8': 'Chemoattractive',
                      'IL-9': 'TH2 Pro Inflammatory',
                      'IP-10': 'Chemoattractive',
                      'MCP-1': 'Chemoattractive',
                      'MCP-4': 'Chemoattractive',
                      'MIP-1a': 'Chemoattractive',
                      'MIP-1b': 'Chemoattractive',
                      'Perforin': 'Cytolytic',
                      'RANTES': 'Chemoattractive',
                      'TGF-b1': 'Regulatory',
                      'TNF-a': 'TH1 Pro Inflammatory',
                      'TNF-b': 'TH1 Pro Inflammatory',
                      'sCD137': 'Other',
                      'sCD40L': 'Other'}

human_innate_immune = {'BCA-1': 'Chemoattractive',
                       'CCL11': 'Chemoattractive',
                       'EGF': 'Growth Factors',
                       'GM-CSF': 'Stimulatory',
                       'IFN-g': 'Effector',
                       'IL-10': 'Regulatory',
                       'IL-12': 'Inflammatory',
                       'IL-12-p40': 'Inflammatory',
                       'IL-13': 'Regulatory',
                       'IL-15': 'Stimulatory',
                       'IL-17a': 'Inflammatory',
                       'IL-17f': 'Inflammatory',
                       'IL-18': 'Stimulatory',
                       'IL-1b': 'Inflammatory',
                       'IL-22': 'Regulatory',
                       'IL-5': 'Stimulatory',
                       'IL-6': 'Inflammatory',
                       'IL-8': 'Stimulatory',
                       'IL-9': 'Stimulatory',
                       'IP-10': 'Chemoattractive',
                       'MCP-1': 'Inflammatory',
                       'MCP-4': 'Inflammatory',
                       'MIF': 'Inflammatory',
                       'MIP-1a': 'Effector',
                       'MIP-1b': 'Chemoattractive',
                       'PDGF-BB': 'Growth Factors',
                       'RANTES': 'Chemoattractive',
                       'TGF-a': 'Stimulatory',
                       'TNF-a': 'Effector',
                       'TNF-b': 'Effector',
                       'VEGF': 'Growth Factors',
                       'sCD40L': 'Regulatory'}

centerStyle = {'textAlign': 'center'}


app = dash.Dash(
    __name__, plugins=[dl.plugins.pages],
    external_stylesheets=[
        dbc.themes.FLATLY],
    # suppress_callback_exceptions set to True for dynamic layout
    suppress_callback_exceptions=True
)

# code for navigation bar
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
# code for user file upload
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
            # this column creates a new column which combines all of the descriptions
            df['Treatment Conditions'] = df[description_list].apply(
                lambda x: ' '.join(x.dropna().astype(str)),
                axis=1)
            # this list will be allow the user to plot graphs in desired order
            df_labels_un = list(df['Treatment Conditions'].unique())
            # heatmap index positions maintained for cells
            num_cells = range(1, len(df)+1)
            df['Permanent Index'] = num_cells
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            df['Treatment Conditions'] = df[description_list].apply(
                lambda x: ' '.join(x.dropna().astype(str)),
                axis=1)
            # this list will be allow the user to plot graphs in desired order
            df_labels_un = list(df['Treatment Conditions'].unique())
            # heatmap index positions maintained for cells
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
        # this stores the data to be used for future callbacks
        dcc.Store(id='stored-data', data=df.to_dict('records')),
        html.H4('Step 2: Select the Assay used for the Isoplexis Analysis: ', style={
                'textAlign': 'left'}),
        html.P("This will determine the cytokines read for the assay.",
               style={'textAlign': 'left'}),
        dcc.RadioItems(
            id="secretome_type",
            options=secretome_selection,
            value="Mouse Adaptive Immune",
            inline=True, inputStyle={"margin-right": "5px", "margin-left": "5px"},
            style=centerStyle),
        html.H4('Step 3: Select the Conditions that will be Analyzed:',
                style={'textAlign': 'left'}),
        html.P("Note: The order (left to right) of items selected will be the same order for the graphs. ", style={
               'textAlign': 'left'}),
        # list for user to reorder data
        dcc.Dropdown(
            id="ordered_list",
            options=df_labels_un,
            multi=True),
        html.Button(id="submit-button", children="Reorder Data"),
        html.H4('Step 4: Select the Button Below to Analyze Isoplexis Data:', style={
                'textAlign': 'left'}),
        html.Div(html.Button(id="analysis-button",
                 children="Analyze Isoplexis Data"), style={'textAlign': 'left'}),
        html.P('Note: If you decide to reorder your data after selecting the analysis button, you will need to repeat steps 3 and 4 again.',
               style={'textAlign': 'left'}),
        html.H4("Step 5: To view individual cytokine analysis, select a cytokine from this list below.", style={
                'textAlign': 'left'}),
        html.P("Note: each analysis page has a section to view individual cytokines. If the cytokine has no value, it will not appear on this list.", style={
               'textAlign': 'left'}),
        html.Div(dcc.Dropdown(
            id='indiv_cyto_dropdown',
            placeholder="Select a cytokine for individual cytokine analysis",
            clearable=False),
            style={"width": "50%"}),

        html.Div(html.Button(id="indiv-cyto-button",
                 children="Analyze Individual Cytokine"), style={'textAlign': 'left'}),
        html.P("In order to change individual cytokine, select desired cytokine from the dropdown menu and click 'Analyze Individual Cytokine' button again.", style={
               'textAlign': 'left'})

    ])


app.layout = dbc.Container(
    [navbar,
     # header
     html.H1('Isoplexis Single Cell Secretome Data Analysis', style=centerStyle),
     html.H2('Suzette Palmer', style=centerStyle),
     html.H3('Zhan and Koh Labs', style=centerStyle),
     html.H4('University of Texas Southwestern Medical Center', style=centerStyle),
     # user file input
     html.H4('Step 1: Upload Isoplexis Data Analysis File:'),
     html.P('Note: Formats allowed are comma separated values (csv) or excel (xls).'),
     userInput,
     # output file information
     html.Div(id='output-data-upload', style=centerStyle),
     dcc.Store(id='cyto_list'),
     dcc.Store(id='effector_list'),
     dcc.Store(id='stored-data-reordered'),
     dcc.Store(id='color_discrete_map'),
     dl.plugins.page_container], fluid=True)


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
              Output('effector_list', 'data'),
              Input('secretome_type', 'value'))
def cyto_secretion_list(val):
    if val is None:
        raise PreventUpdate

    else:
        if val == "Mouse Adaptive Immune":
            cyto_list = list(mouse_adaptive_immune.keys())
            effector_list = mouse_adaptive_immune
        elif val == 'Human Adaptive Immune':
            cyto_list = list(human_adaptive_immune.keys())
            effector_list = human_adaptive_immune
        elif val == 'Non-Human Primate Adaptive Immune':
            cyto_list = list(nhp_adaptive_immune.keys())
            effector_list = nhp_adaptive_immune
        elif val == 'Human Inflammation':
            cyto_list = list(human_inflammation.keys())
            effector_list = human_inflammation
        else:
            # elif val == 'Human Innate Immune':
            cyto_list = list(human_innate_immune.keys())
            effector_list = human_innate_immune
        return cyto_list, effector_list


@app.callback(Output('stored-data-reordered', 'data'),
              Input('submit-button', 'n_clicks'),
              State('ordered_list', 'value'),
              Input('stored-data', 'data'))
def permutationToPlot(n, selected_permutation, data):
    if n is None:
        data = pd.DataFrame(data)
        return data.to_dict('records')
    else:
        data = pd.DataFrame(data)
        # this function reorders the dataframe so user can select which order to plot
        count = 0
        for i in selected_permutation:
            if count == 0:
                new_data = data[data["Treatment Conditions"] == i]
                count = count + 1
            else:
                df_to_append = data[data["Treatment Conditions"] == i]
                new_data = pd.concat([new_data, df_to_append])
                count = count + 1
        return new_data.to_dict('records')

# this makes sure the color schemes for the bar plots, density and histogram are consistent


@app.callback(Output('color_discrete_map', 'data'),
              Input('submit-button', 'n_clicks'),
              State('ordered_list', 'value'))
def discrete_color(n, selected_permutation):
    if n is None:
        return no_update
    else:
        # this makes sure colors are the same for bar plots, density and histogram
        #"blue", "red", "gray", "green", "yellow", "teal", "purple", "black"
        colors = ['rgb(255, 0, 0)', 'rgb(0, 0, 255)', 'rgb(128, 128, 128)', 'rgb(0, 128, 0)',
                  'rgb(255, 255, 0)', 'rgb(0, 128, 128)', 'rgb(128, 0, 128)', 'rgb(0, 0, 0)']
        colors_for_plot = colors[:len(selected_permutation)]
        color_discrete_map = {selected_permutation[i]: colors_for_plot[i] for i in range(
            len(selected_permutation))}
        return color_discrete_map


@app.callback(
    Output('indiv_cyto_dropdown', 'options'),
    Input('submit-button', 'n_clicks'),
    Input('indiv-cyto-button', 'n_clicks'),
    State('cyto_list', 'data'),
    State('ordered_list', 'value'),
    State('stored-data-reordered', 'data'))
def individual_cyto_callback(n, m, cyto_list, selected_cytokine, df):
    if (n is None) and (m is None):
        return no_update

    else:
        df = pd.DataFrame(df)
        # create an edited cytokine list for dropdown
        # columns with no values will be removed
        edit_cyto_list = []
        for i in cyto_list:
            if df[i].sum() == 0:
                continue
            else:
                edit_cyto_list.append(i)
        # create dictionary for dynamic callbacks for dendrogram and heatmap
        heatmap_dictionary = []
        for cytokine in edit_cyto_list:
            small_list = ["All"]
            for i in selected_cytokine:
                sub_vals = df.loc[df["Treatment Conditions"] == i, cytokine]
                if sub_vals.sum() != 0:
                    # not sure if either or both is needed for this
                    small_list.append(i)
            heatmap_dictionary.append(small_list)
        # using dictionary comprehension to convert lists to dictionary
        # main dictionary used for the callbacks.
        cytokine_dictionary = {
            edit_cyto_list[i]: heatmap_dictionary[i] for i in range(len(edit_cyto_list))}
        options = [{'label': k, 'value': k}
                   for k in cytokine_dictionary.keys()]
        return options


if __name__ == "__main__":
    print(dash.__version__)
    app.run_server(debug=True)
