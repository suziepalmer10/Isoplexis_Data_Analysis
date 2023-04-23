import base64
import datetime
import io
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
from dash import no_update
import plotly.express as px
from dash import dcc, html, Input, Output, callback
import dash
from dash.exceptions import PreventUpdate
from sklearn import preprocessing
from os.path import basename, getmtime

# dash.register_page(__name__, title='Upload')

centerStyle = {"textAlign": "center"}


description_list = ["Donor", "Cell Subset", "Stimulation"]

secretome_selection = [
    "Mouse Adaptive Immune",
    "Human Adaptive Immune",
    "Non-Human Primate Adaptive Immune",
    "Human Inflammation",
    "Human Innate Immune",
]

pre_specified_filename = 'assets/WT_ABX_MLN_T_Cell_CD4+_CD8+_raw_data.csv'
    
use_prespecified_button = dbc.Button(
      "Upload Example",
      id='use-preset-file', n_clicks=0
)

    # code for user file upload
userInput = dcc.Upload(
        id="upload-data",
        children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
        style={
            "width": "100%",
            "height": "60px",
            "lineHeight": "60px",
            "borderWidth": "1px",
            "borderStyle": "dashed",
            "borderRadius": "5px",
            "textAlign": "center",
            "margin": "0px",
        },
        # Allow multiple files to be uploaded
        multiple=True,
    )

    
    


upload_data_summary = html.Div(
    [
        html.H4(id="check_cyto_num"),
        html.P(id="warning1"),
        html.P(id="row_value"),
        html.P(id="col_value"),
    ],
    style=centerStyle,
)


layout = html.Div(
    [
        # user file input
        html.H2("Data Preparation", style=centerStyle),
        html.Div(
            [
                html.H4(
                    "Step 1: Upload Isoplexis Data Analysis File:",
                    style={"textAlign": "left"},
                ),
                html.P(
                    [
                        html.I(className="fa fa-sticky-note"),
                        "Note: Formats allowed are comma separated values (csv) or excel (xls). See: ",
                        html.A(
                            "CSV example",
                            href="assets/WT_ABX_MLN_T_Cell_CD4+_CD8+_raw_data.csv",
                            #draggable = 'true', 
                            target = '_parent'
                        ),
                        " or ",
                        html.A("Excel example", href="assets/isoplexis_raw_data.xlsx"),
                        ".",
                    ]
                ),
                use_prespecified_button, 
                userInput,
                html.Br(),
                # output file information
                html.Div(id="output-data-upload", style=centerStyle),
                dcc.Store(id="cyto_list"),
                dcc.Store(id="effector_list"),
                dcc.Store(id="stored-data-reordered"),
                dcc.Store(id="color_discrete_map"),
                dcc.Store(id="filtered-data"),
                #dcc.Store(id = "new-cyto-list")
            ],
            className="shadow p-3 mb-5 bg-white rounded",
        ),
        # step 2- 5
        html.Div(
            [
                # this stores the data to be used for future callbacks
                dcc.Store(id="stored-data"),
                html.Div(
                    [
                        html.H4(
                            "Step 2: Select the Assay used for the Isoplexis Analysis: ",
                            style={"textAlign": "left"},
                        ),
                        html.P(
                            "This will determine the cytokines read for the assay.",
                            style={"textAlign": "left"},
                        ),
                        dcc.RadioItems(
                            id="secretome_type",
                            options=secretome_selection,
                            value="Mouse Adaptive Immune",
                            inline=True,
                            inputStyle={"margin-right": "5px", "margin-left": "5px"},
                            style=centerStyle,
                        ),
                    ],
                    className="shadow p-3 mb-5 bg-white rounded",
                ),
                html.Div(
                    [
                        html.H4(
                            "Step 3: Select the Conditions that will be Analyzed:",
                            style={"textAlign": "left"},
                        ),
                        html.P(
                            [
                                html.I(className="fa fa-sticky-note"),
                                "Note: The order (left to right) of items selected will be the same order for the graphs. ",
                            ],
                            style={"textAlign": "left"},
                        ),
                        # list for user to reorder data
                        dcc.Dropdown(
                            id="ordered_list",
                            # TODO: options=df_labels_un,
                            multi=True,
                            placeholder="Select conditions to analyze",
                        ),
                        html.Button(id="submit-button", children="Reorder Data"),
                    ],
                    className="shadow p-3 mb-5 bg-white rounded",
                ),
                
                html.Div(
                    [
                        html.H4(
                            "Step 4: Filter and Normalize data.",
                            style={"textAlign": "left"},
                        ),
                        html.P(
                            [
                                '(Optinoal) Select method of normalization and/or scaling ',
                                html.Span(
                                    "(details)",
                                    id="tooltip-target",
                                    style={"textDecoration": "underline", "cursor": "pointer"},
                                ),
                                dbc.Tooltip(
                                    "Log Scale: Log10 transformation of data. Normalize by Cytokine: Normalizes data by cytokine. Log Scale and Normalize by Cytokine: Log10 transformation of data and then normalizes by cytokine.",
                                    target="tooltip-target",
                                ), 
                                dcc.RadioItems(['None', 'Log Scale', 'Normalize by Cytokine', 'Log Scale and Normalize by Cytokine'], 'None',
                                    inline = True, id = 'normalize-condition', 
                                    inputStyle={
                                        "margin-right": "5px",
                                        "margin-left": "5px",
                                    },
                                    style=centerStyle,),
                            ]),
                        # list for user to reorder data
                        ########
                        # dcc.Dropdown(
                        #     id="ordered_list",
                        #     # TODO: options=df_labels_un,
                        #     multi=True,
                        #     placeholder="Select to filter ",
                        # ),
                        html.P('User can remove cells that do not express any cytokines.'),
                        dcc.RadioItems(['None', 'All'], 'None', inline=True, id = 'filter-condition',
                                       inputStyle={
                                           "margin-right": "5px",
                                           "margin-left": "5px",
                                       },
                                       style=centerStyle),
                        html.Button(id="filtered-button", children="Filter Data"),
                        html.P(
                            [
                                html.I(className="fa fa-sticky-note"),
                                "Note: The default is set to none. If All is selected cells that do not express any cytokines will be removed from the dataset.  ",
                            ],
                            style={"textAlign": "left"},
                        ),
                    ],
                    className="shadow p-3 mb-5 bg-white rounded",
                ),
                
                
                
                html.Div(
                    [
                        html.H4(
                            "Step 5: Select the Button Below to Analyze Isoplexis Data:",
                            style={"textAlign": "left"},
                        ),
                        html.Div(
                            html.Button(
                                id="analysis-button", children="Analyze Isoplexis Data"
                            ),
                            style={"textAlign": "left"},
                        ),
                        html.P(
                            [
                                html.I(className="fa fa-sticky-note"),
                                "Note: If you decide to reorder your data after selecting the analysis button, you will need to repeat steps 3 and 4 again.",
                            ],
                            style={"textAlign": "left"},
                        ),
                        html.Div(
                            upload_data_summary,
                            id="upload-data-summary",
                            style={"display": "none"},
                            className="border border-danger",
                        ),
                    ],
                    className="shadow p-3 mb-5 bg-white rounded",
                ),
                html.Div(
                    [
                        html.H4(
                            "Step 6: To view individual cytokine analysis, select a cytokine from this list below.",
                            style={"textAlign": "left"},
                        ),
                        html.P(
                            [
                                html.I(className="fa fa-sticky-note"),
                                "Note: each analysis page has a section to view individual cytokines. If the cytokine has no value, it will not appear on this list.",
                            ],
                            style={"textAlign": "left"},
                        ),
                        html.Div(
                            dcc.Dropdown(
                                id="indiv_cyto_dropdown",
                                placeholder="Select a cytokine for individual cytokine analysis",
                                clearable=False,
                            ),
                            style={"width": "50%"},
                        ),
                        html.Div(
                            html.Button(
                                id="indiv-cyto-button",
                                children="Analyze Individual Cytokine",
                            ),
                            style={"textAlign": "left"},
                        ),
                        html.P(
                            "In order to change individual cytokine, select desired cytokine from the dropdown menu and click 'Analyze Individual Cytokine' button again.",
                            style={"textAlign": "left"},
                        ),
                    ],
                    className="shadow p-3 mb-5 bg-white rounded",
                ),
            ],
            id="step2-5",
            style={"display": "none"},
        ),
    ]
)

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
            # this column creates a new column which combines all of the descriptions
            df["Treatment Conditions"] = df[description_list].apply(
                lambda x: " ".join(x.dropna().astype(str)), axis=1
            )
            # this list will be allow the user to plot graphs in desired order
            df_labels_un = list(df["Treatment Conditions"].unique())
            # heatmap index positions maintained for cells
            num_cells = range(1, len(df) + 1)
            df["Permanent Index"] = num_cells
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            df["Treatment Conditions"] = df[description_list].apply(
                lambda x: " ".join(x.dropna().astype(str)), axis=1
            )
            # this list will be allow the user to plot graphs in desired order
            df_labels_un = list(df["Treatment Conditions"].unique())
            # heatmap index positions maintained for cells
            num_cells = range(1, len(df) + 1)
            df["Permanent Index"] = num_cells
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])

    return {
        "layout": html.Div(
            [
                html.I(className="fa fa-info"),
                html.H4("Uploaded File Information: ", style=centerStyle),
                html.P(["File name: ", filename]),
                html.P(["Timestamp: ", datetime.datetime.fromtimestamp(date)]),
            ],
            className="border border-info",
        ),
        "df_labels_un": df_labels_un,
        "df": df.to_dict("records"),
    }

@callback(
    Output("output-data-upload", "children"),
    Output("stored-data", "data"),
    Output("ordered_list", "options"),
    Output("step2-5", "style"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    State("upload-data", "last_modified"),
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    print("contents =", str(list_of_contents)[:100])
    print("list_of_names =", list_of_names) 
    print("list_of_dates =", list_of_dates)   
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d)
            for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
        ]
        if len(children) != 1:
            print("Uploaded multiple files but only the first will be processed")
        return [
            children[0]["layout"],
            children[0]["df"],
            children[0]["df_labels_un"],
            {"display": "block"},
        ]
    else:
        return [no_update, no_update, no_update, {"display": "none"}]


@callback(
    Output("row_value", "children"),
    Output("col_value", "children"),
    Output("check_cyto_num", "children"),
    Output("warning1", "children"),
    Output("upload-data-summary", "style"),
    Input("analysis-button", "n_clicks"),
    #Input("filtered-button", "n_clicks"),
    Input("cyto_list", "data"),
    #State("stored-data-reordered", "data"),
    State("filtered-data", "data"),
    prevent_initial_call=True,
)
def col_row_check(n, cyto_list, df):
    if (n is None) :
        raise PreventUpdate
    else:
        df = pd.DataFrame(df)
        df_sub = df[cyto_list].T
        row, col = df_sub.shape
        numCytokines = "Number of Cytokines: " + str(row)
        numCells = "Number of Cells: " + str(col)
        check_cyto_num = html.Div(
            [
                html.I(className="fa fa-eye"),
                html.P(
                    "Please ensure that the number of cytokines and the number of cells displayed below are correct before proceeding."
                ),
            ]
        )
        warning1 = "If these numbers are off, double-check your original csv or excel file and also ensure the selected secretome assay is correct."
        return (numCytokines, numCells, check_cyto_num, warning1, {"display": "block"})

@callback(
    Output('upload-data', 'contents'),
    Output("upload-data", "filename"),
    Output("upload-data", "last_modified"),
    Input('use-preset-file', 'n_clicks'),
)
def upload_preset_file(n_clicks):
    if n_clicks > 0:
        with open(pre_specified_filename, "rb") as f:
            contents = base64.b64encode(f.read()).decode("utf-8")
            return [[f'data:text/csv;base64,{contents}'],
                    [basename(pre_specified_filename)],
                    [getmtime(pre_specified_filename)]]
    return [None, None, None]