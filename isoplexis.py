import pages.Contact
import pages.Statistics
import pages.Polyfunctionality
import pages.DimensionalityReduction
import pages.Clustering
import pages.Upload
import pages.Overview
import pages.Contact

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
from dash import no_update

# this is the original description list

mouse_adaptive_immune = {
    "BCA-1": "Chemoattractive",
    "CCL-11": "Chemoattractive",
    "FAS": "Regulatory",
    "GM-CSF": "Stimulatory",
    "Granzyme B": "Effector",
    "IFN-g": "Effector",
    "IL-10": "Regulatory",
    "IL-12p70": "Stimulatory",
    "IL-13": "Regulatory",
    "IL-15": "Stimulatory",
    "IL-17A": "Inflammatory",
    "IL-18": "Stimulatory",
    "IL-1b": "Inflammatory",
    "IL-2": "Stimulatory",
    "IL-21": "Stimulatory",
    "IL-27": "Regulatory",
    "IL-4": "Regulatory",
    "IL-5": "Stimulatory",
    "IL-6": "Inflammatory",
    "IL-7": "Stimulatory",
    "IP-10": "Chemoattractive",
    "KC": "Chemoattractive",
    "MCP-1": "Inflammatory",
    "MIP-1a": "Effector",
    "RANTES": "Chemoattractive",
    "sCD137": "Stimulatory",
    "TGF-b": "Regulatory",
    "TNF-a": "Effector",
}

human_adaptive_immune = {
    "CCL-11": "Chemoattractive",
    "GM-CSF": "Stimulatory",
    "Granzyme B": "Effector",
    "IFN-g": "Effector",
    "IL-10": "Regulatory",
    "IL-12": "Stimulatory",
    "IL-13": "Regulatory",
    "IL-15": "Stimulatory",
    "IL-17a": "Inflammatory",
    "IL-17f": "Inflammatory",
    "IL-1b": "Inflammatory",
    "IL-2": "Stimulatory",
    "IL-21": "Stimulatory",
    "IL-22": "Regulatory",
    "IL-4": "Regulatory",
    "IL-5": "Stimulatory",
    "IL-6": "Inflammatory",
    "IL-7": "Stimulatory",
    "IL-8": "Stimulatory",
    "IL-9": "Stimulatory",
    "IP-10": "Chemoattractive",
    "MCP-1": "Inflammatory",
    "MCP-4": "Inflammatory",
    "MIP-1a": "Effector",
    "MIP-1b": "Chemoattractive",
    "Perforin": "Effector",
    "RANTES": "Chemoattractive",
    "TGF-b1": "Regulatory",
    "TNF-a": "Effector",
    "TNF-b": "Effector",
    "sCD137": "Regulatory",
    "sCD40L": "Regulatory",
}

nhp_adaptive_immune = {
    "GM-CSF": "Stimulatory",
    "IFN-g": "Effector",
    "IL-1b": "Inflammatory",
    "IL-2": "Stimulatory",
    "IL-4": "Regulatory",
    "IL-6": "Inflammatory",
    "IL-8": "Stimulatory",
    "IP-10": "Chemoattractive",
    "MCP-1": "Inflammatory",
    "MIF": "Inflammatory",
    "MIP-1a": "Effector",
    "MIP-1b": "Chemoattractive",
    "RANTES": "Chemoattractive",
    "TNF-a": "Effector",
}

human_inflammation = {
    "CCL11": "Chemoattractive",
    "GM-CSF": "TH1 Pro Inflammatory",
    "Granzyme B": "Cytolytic",
    "IFN-g": "TH1 Pro Inflammatory",
    "IL-10": "Regulatory",
    "IL-12": "TH1 Pro Inflammatory",
    "IL-13": "TH2 Pro Inflammatory",
    "IL-15": "Regulatory",
    "IL-17a": "TH17 Pro Inflammatory",
    "IL-17f": "TH17 Pro Inflammatory",
    "IL-1b": "TH17 Pro Inflammatory",
    "IL-2": "TH1 Pro Inflammatory",
    "IL-21": "TH17 Pro Inflammatory",
    "IL-22": "Regulatory",
    "IL-4": "TH2 Pro Inflammatory",
    "IL-5": "TH2 Pro Inflammatory",
    "IL-6": "TH17 Pro Inflammatory",
    "IL-7": "TH2 Pro Inflammatory",
    "IL-8": "Chemoattractive",
    "IL-9": "TH2 Pro Inflammatory",
    "IP-10": "Chemoattractive",
    "MCP-1": "Chemoattractive",
    "MCP-4": "Chemoattractive",
    "MIP-1a": "Chemoattractive",
    "MIP-1b": "Chemoattractive",
    "Perforin": "Cytolytic",
    "RANTES": "Chemoattractive",
    "TGF-b1": "Regulatory",
    "TNF-a": "TH1 Pro Inflammatory",
    "TNF-b": "TH1 Pro Inflammatory",
    "sCD137": "Other",
    "sCD40L": "Other",
}

human_innate_immune = {
    "BCA-1": "Chemoattractive",
    "CCL11": "Chemoattractive",
    "EGF": "Growth Factors",
    "GM-CSF": "Stimulatory",
    "IFN-g": "Effector",
    "IL-10": "Regulatory",
    "IL-12": "Inflammatory",
    "IL-12-p40": "Inflammatory",
    "IL-13": "Regulatory",
    "IL-15": "Stimulatory",
    "IL-17a": "Inflammatory",
    "IL-17f": "Inflammatory",
    "IL-18": "Stimulatory",
    "IL-1b": "Inflammatory",
    "IL-22": "Regulatory",
    "IL-5": "Stimulatory",
    "IL-6": "Inflammatory",
    "IL-8": "Stimulatory",
    "IL-9": "Stimulatory",
    "IP-10": "Chemoattractive",
    "MCP-1": "Inflammatory",
    "MCP-4": "Inflammatory",
    "MIF": "Inflammatory",
    "MIP-1a": "Effector",
    "MIP-1b": "Chemoattractive",
    "PDGF-BB": "Growth Factors",
    "RANTES": "Chemoattractive",
    "TGF-a": "Stimulatory",
    "TNF-a": "Effector",
    "TNF-b": "Effector",
    "VEGF": "Growth Factors",
    "sCD40L": "Regulatory",
}

centerStyle = {"textAlign": "center"}


app = dash.Dash(
    __name__,
    external_stylesheets=[
         dbc.themes.FLATLY,
        # dbc.icons.BOOTSTRAP,
        dbc.icons.FONT_AWESOME
    ],
    # suppress_callback_exceptions set to True for dynamic layout
    suppress_callback_exceptions=True,
    #use_pages=False,
    title = "Isoplexis Data Analysis"
)

# code for navigation bar
navbar = dbc.Navbar(
    [
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src="assets/favicon.ico", height="30px")),
                            dbc.Col(
                                dbc.NavbarBrand(
                                    "Isoplexis Data Analysis",
                                    className="ms-2",
                                    style={"color": "white"},
                                )
                            ),
                        ],
                        # align="center",
                        className="g-0",
                    ),
                    href="#",
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.A(
                                    dbc.Button(
                                        [html.I(className="fa-brands fa-twitter"), ""],
                                        color="light",
                                    ),
                                    href="https://twitter.com/intent/tweet?text=Tweet%20from%20Isoplexis%20Data%20Analysis",
                                )
                            ),
                            dbc.Col(
                                html.A(
                                    dbc.Button(
                                        [html.I(className="fa-brands fa-github"), ""],
                                        color="light",
                                    ),
                                    href="https://github.com/suziepalmer10/Isoplexis_Data_Analysis",
                                    target="_blank",
                                )
                            ),
                            dbc.Col(
                                html.A(
                                    dbc.Button(
                                        [html.I(className="fa fa-envelope"), ""],
                                        color="light",
                                    ),
                                    href="mailto:suzette.palmer@utsouthwestern.edu?cc=xiaowei.zhan@utsouthwestern.edu",
                                )
                            ),
                        ],
                        className="g-1 ms-auto flex-nowrap mt-3 mt-md-0",
                        align="center",
                    ),
                    id="navbar-collapse",
                    is_open=True,
                    navbar=True,
                ),
            ],
            className="d-grid gap-2 d-md-flex justify-content-md-end",
        )
    ],
    # brand="Isoplexis Data Analysis",
    # brand_href="#",
    color="primary"
    # dark=True,
    # className="mb-2",
)


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


layouts = {
    "tab-overview": (pages.Overview.layout),
    "tab-upload": pages.Upload.layout,
    "tab-clustering": pages.Clustering.layout,
    "tab-dimensionreduction": pages.DimensionalityReduction.layout,
    "tab-polyfunctionality": pages.Polyfunctionality.layout,
    "tab-statistics": pages.Statistics.layout,
    "tab-contact": pages.Contact.layout,
}

footer = html.Footer(
    html.Div(
        html.P(
            [
                "2022 ©",
                html.A(
                    "Zhan lab",
                    href="https://www.utsouthwestern.edu/labs/zhan/",
                    target="_blank",
                    style={"text-decoration": "none"},
                ),
                " | ",
                html.A(
                    "Koh lab",
                    href="https://kohlab.org",
                    target="_blank",
                    style={"text-decoration": "none"},
                ),
                " | ",
                html.A(
                    "Quantitative Biomedical Research Center",
                    href="https://qbrc.swmed.edu",
                    target="_blank",
                    style={"text-decoration": "none"},
                ),
                " | ",
                html.A(
                    "UT Southwestern Medical Center",
                    href="https://www.utsouthwestern.edu",
                    target="_blank",
                    style={"text-decoration": "none"},
                ),
            ]
        ),
        style={"textAlign": "center", "color": "#fff"},
    ),
    className="bg-primary footer",
)

app.layout = html.Div(
    [
        navbar,
        dbc.Container(
            dcc.Tabs(
                id="tabs-header",
                children=[
                    dcc.Tab(label="Overview", children=layouts["tab-overview"]),
                    dcc.Tab(label="Upload", children=layouts["tab-upload"]),
                    dcc.Tab(label="Clustering", children=layouts["tab-clustering"]),
                    dcc.Tab(
                        label="Dimension Reduction",
                        children=layouts["tab-dimensionreduction"],
                    ),
                    dcc.Tab(
                        label="Polyfunctionality",
                        children=layouts["tab-polyfunctionality"],
                    ),
                    dcc.Tab(label="Statistics", children=layouts["tab-statistics"]),
                    #            dcc.Tab(label='Contact', children=layouts['tab-contact']),
                ],
            )
        ),
        footer,
    ]
)


@app.callback(
    Output("cyto_list", "data"),
    Output("effector_list", "data"),
    Input("secretome_type", "value"),
)
def cyto_secretion_list(val):
    if val is None:
        raise PreventUpdate

    else:
        if val == "Mouse Adaptive Immune":
            cyto_list = list(mouse_adaptive_immune.keys())
            effector_list = mouse_adaptive_immune
        elif val == "Human Adaptive Immune":
            cyto_list = list(human_adaptive_immune.keys())
            effector_list = human_adaptive_immune
        elif val == "Non-Human Primate Adaptive Immune":
            cyto_list = list(nhp_adaptive_immune.keys())
            effector_list = nhp_adaptive_immune
        elif val == "Human Inflammation":
            cyto_list = list(human_inflammation.keys())
            effector_list = human_inflammation
        else:
            # elif val == 'Human Innate Immune':
            cyto_list = list(human_innate_immune.keys())
            effector_list = human_innate_immune
        return cyto_list, effector_list


@app.callback(
    Output("stored-data-reordered", "data"),
    Input("submit-button", "n_clicks"),
    State("ordered_list", "value"),
    Input("stored-data", "data"),
)
def permutationToPlot(n, selected_permutation, data):
    if n is None:
        data = pd.DataFrame(data)
        return data.to_dict("records")
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
        return new_data.to_dict("records")


# this makes sure the color schemes for the bar plots, density and histogram are consistent


@app.callback(
    Output("color_discrete_map", "data"),
    Input("submit-button", "n_clicks"),
    State("ordered_list", "value"),
)
def discrete_color(n, selected_permutation):
    if n is None:
        return no_update
    else:
        # this makes sure colors are the same for bar plots, density and histogram
        # "blue", "red", "gray", "green", "yellow", "teal", "purple", "black"
        colors = [
            "rgb(255, 0, 0)",
            "rgb(0, 0, 255)",
            "rgb(128, 128, 128)",
            "rgb(0, 128, 0)",
            "rgb(255, 255, 0)",
            "rgb(0, 128, 128)",
            "rgb(128, 0, 128)",
            "rgb(0, 0, 0)",
        ]
        colors_for_plot = colors[: len(selected_permutation)]
        color_discrete_map = {
            selected_permutation[i]: colors_for_plot[i]
            for i in range(len(selected_permutation))
        }
        return color_discrete_map


@app.callback(
    Output("indiv_cyto_dropdown", "options"),
    Input("submit-button", "n_clicks"),
    Input("indiv-cyto-button", "n_clicks"),
    State("cyto_list", "data"),
    State("ordered_list", "value"),
    State("stored-data-reordered", "data"),
)
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
            edit_cyto_list[i]: heatmap_dictionary[i] for i in range(len(edit_cyto_list))
        }
        options = [{"label": k, "value": k} for k in cytokine_dictionary.keys()]
        return options


if __name__ == "__main__":
    print(dash.__version__)
    app.run_server(debug=True)
