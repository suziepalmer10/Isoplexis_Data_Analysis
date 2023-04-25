import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
from dash import no_update
import plotly.express as px
from dash import dcc, html, Input, Output, callback
import dash

centerStyle = {'textAlign': 'center'}


layout = html.Div(
    [
      html.H1('Isoplexis Single Cell Secretome Data Analysis',
                      style=centerStyle),
              html.P('Suzette Palmer', style=centerStyle),
          html.P('Zhan and Koh Labs', style=centerStyle),
              html.P('University of Texas Southwestern Medical Center',
                     style=centerStyle)
                     ]
)
