import pandas as pd
import re
import io
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import base64
import datetime
from datetime import datetime
import time
import dash_bootstrap_components as dbc

image_filename = 'domatec_logo.png'  # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
Messungen = []


def iterprete_txt_file(datei):
    volume = ''
    Flow = 0.0
    Duration = 0.0
    Interval = 0.0
    Intervals = 0.0
    Hardwarerevision = 0.0
    Softwareversion = ''
    Mesurement_status = ''
    Messdaten = []

    for line in io.StringIO(datei):
        if line.startswith('#Volume'):
            volume = float(re.findall(r'\d+', line)[0])
        if line.startswith('#Flow'):
            Flow = float(re.findall(r'\d+', line)[0])
        if line.startswith('#Duration'):
            Duration = float(re.findall(r'\d+', line)[0])
        if line.startswith('#Interval '):
            Interval = float(re.findall(r'\d+', line)[0])
        if line.startswith('#Intervals'):
            Intervals = float(re.findall(r'\d+', line)[0])
        if line.startswith('#Hardwarerevision'):
            Hardwarerevision = re.findall(r'\d+', line)[0]
        if line.startswith('#Softwareversion'):
            Softwareversion = re.findall(r'\d+', line)[0]
        if line.startswith('#Measurement'):
            Mesurement_status = line[1:]
        if line.startswith('#Date'):
            line.replace('°', 'Grad ')
            Messdaten.append(line[1:])
        if not line.startswith('#'):
            Messdaten.append(line)

    df = pd.read_csv(io.StringIO('\n'.join(Messdaten)), sep=';')
    df[' Time'] = df[' Time'].apply(lambda x: datetime.strptime(x, '%H:%M:%S'))
    df['Duration [min]'] = df[' Time'].apply(lambda x: (x - df[' Time'][0]).total_seconds() / 60)
    df[' Time'] = df[' Time'].apply(lambda x: x.time())
    df = df.rename(columns={df.columns[8]: 'TempAkku1 [°C]'})
    df = df.rename(columns={df.columns[9]: 'TempAkku2 [°C]'})
    df = df.rename(columns={df.columns[10]: 'TempPump [°C]'})
    df = df.rename(columns={df.columns[11]: 'TempDCDC [°C]'})

    return volume, Flow, Duration, Interval, Intervals, Hardwarerevision, Softwareversion, Mesurement_status, df


# Text field
def drawImg():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    dbc.Col([html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                                      style={'height': '100%', 'width': '100%'})]),
                ],
                )
            ])
        ),
    ])


def drawText():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    dbc.Col([html.H1('Mykotoxinsammler Dashboard')]),
                ],
                )
            ])
        ),
    ])


def x_dropdown(id):
    items = [
        {'label': "Date", 'value': "Date"},
        {'label': "Duration [min]", 'value': "Duration [min]"},
        {'label': " Time", 'value': " Time"},
        {'label': " Volume[SL]", 'value': " Volume[SL]"},
        {'label': " Flow[SdL/min]", 'value': " Flow[SdL/min]"},
        {'label': " DiffPress[mPa]", 'value': " DiffPress[mPa]"},
        {'label': " Progress[%]", 'value': " Progress[%]"},
        {'label': " PowerStatus", 'value': " PowerStatus"},
        {'label': " Error", 'value': " Error"},
        {'label': "TempAkku1 [°C]", 'value': "TempAkku1 [°C]"},
        {'label': "TempAkku2 [°C]", 'value': "TempAkku2 [°C]"},
        {'label': "TempPump [°C]", 'value': "TempPump [°C]"},
        {'label': "TempDCDC [°C]", 'value': "TempDCDC [°C]"},
        {'label': " Ic[mA]", 'value': " Ic[mA]"},
        {'label': " Ia[mA]", 'value': " Ia[mA]"},
        {'label': " Ua[mV]", 'value': " Ua[mV]"},
        {'label': " DAC", 'value': " DAC"}
    ]
    return dcc.Dropdown(id=id,
                        options=items,
                        multi=False, value=" Time")


def y_dropdown(id):
    items = [
        {'label': "Date", 'value': "Date"},
        {'label': "Duration [min]", 'value': "Duration [min]"},
        {'label': " Time", 'value': " Time"},
        {'label': " Volume[SL]", 'value': " Volume[SL]"},
        {'label': " Flow[SdL/min]", 'value': " Flow[SdL/min]"},
        {'label': " DiffPress[mPa]", 'value': " DiffPress[mPa]"},
        {'label': " Progress[%]", 'value': " Progress[%]"},
        {'label': " PowerStatus", 'value': " PowerStatus"},
        {'label': " Error", 'value': " Error"},
        {'label': "TempAkku1 [°C]", 'value': "TempAkku1 [°C]"},
        {'label': "TempAkku2 [°C]", 'value': "TempAkku2 [°C]"},
        {'label': "TempPump [°C]", 'value': "TempPump [°C]"},
        {'label': "TempDCDC [°C]", 'value': "TempDCDC [°C]"},
        {'label': " Ic[mA]", 'value': " Ic[mA]"},
        {'label': " Ia[mA]", 'value': " Ia[mA]"},
        {'label': " Ua[mV]", 'value': " Ua[mV]"},
        {'label': " DAC", 'value': " DAC"}
    ]

    return dcc.Dropdown(id=id,
                        options=items,
                        multi=False, value=" Volume[SL]")


# Build App
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    drawText()
                ], width=10),
                dbc.Col([
                    drawImg()
                ], width=2),
            ], align='center'),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Upload(
                                    id='upload',
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
                                ),

                            ]))])
                ], width=12),
            ], align='center'),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([html.Div([
                                html.Div(html.H3('Select X-Axis Parameter'),
                                         style={'width': '50%', 'display': 'inline-block'}),
                                html.Div(html.H3('Select Y-Axis Parameter'),
                                         style={'width': '50%', 'display': 'inline-block'}),
                                html.Div(x_dropdown('x_Achse'), style={'width': '50%', 'display': 'inline-block'}),
                                html.Div(y_dropdown('y_Achse'), style={'width': '50%', 'display': 'inline-block'}),

                            ]),

                                dcc.Graph(id='graph',
                                          figure={},
                                          config={
                                              'displayModeBar': False
                                          })
                            ])
                        )
                    ])
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([html.Div([
                                html.Div(html.H3('Select X-Axis Parameter'),
                                         style={'width': '50%', 'display': 'inline-block'}),
                                html.Div(html.H3('Select Y-Axis Parameter'),
                                         style={'width': '50%', 'display': 'inline-block'}),
                                html.Div(x_dropdown('x_Achse_2'), style={'width': '50%', 'display': 'inline-block'}),
                                html.Div(y_dropdown('y_Achse_2'), style={'width': '50%', 'display': 'inline-block'}),

                            ]),

                                dcc.Graph(id='graph_2',
                                          figure={},
                                          config={
                                              'displayModeBar': False
                                          })
                            ])
                        )
                    ])
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Card(
                            dbc.CardBody([html.Div([
                                html.Div(html.H3('Select X-Axis Parameter'),
                                         style={'width': '50%', 'display': 'inline-block'}),
                                html.Div(html.H3('Select Y-Axis Parameter'),
                                         style={'width': '50%', 'display': 'inline-block'}),
                                html.Div(x_dropdown('x_Achse_3'), style={'width': '50%', 'display': 'inline-block'}),
                                html.Div(y_dropdown('y_Achse_3'), style={'width': '50%', 'display': 'inline-block'}),

                            ]),

                                dcc.Graph(id='graph_3',
                                          figure={},
                                          config={
                                              'displayModeBar': False
                                          })
                            ])
                        )
                    ])
                ])
            ])

        ]), color='dark'
    )]

)


@app.callback(
    Output("graph", "figure"),
    [Input("upload", "contents"),
     Input("upload", "filename"),
     Input('y_Achse', 'value'),
     Input('x_Achse', 'value')
     ]
)
def draw_graph(contents, filename, y_parameter, x_paramerter):
    fig = go.Figure()
    colors = ['#636EFA',
              '#EF553B',
              '#00CC96',
              '#AB63FA',
              '#FFA15A',
              '#19D3F3',
              '#FF6692',
              '#B6E880',
              '#FF97FF',
              '#FECB52']
    if not contents is None:
        for idx, content in enumerate(contents):
            content_type, content_string = content.split(',')
            datei = base64.b64decode(content_string).decode('cp1251')
            volume, Flow, Duration, Interval, Intervals, Hardwarerevision, Softwareversion, Mesurement_status, df \
                = iterprete_txt_file(datei)
            fig_new = px.line(df, x=x_paramerter, y=y_parameter, labels=filename[idx]
                              ).update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)'
            )
            fig_new.update_traces(line_color=colors[idx])
            fig = go.Figure(data=fig.data + fig_new.data).update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                xaxis=dict(
                    title=x_paramerter
                ),
                yaxis=dict(
                    title=y_parameter
                )
            )
            fig.data[idx].name = filename[idx]
            fig.data[idx].showlegend = True
        return fig
    else:
        return fig


@app.callback(
    Output("graph_2", "figure"),
    [Input("upload", "contents"),
     Input("upload", "filename"),
     Input('y_Achse_2', 'value'),
     Input('x_Achse_2', 'value')
     ]
)
def draw_graph_2(contents, filename, y_parameter, x_paramerter):
    time.sleep(0.5)
    fig = go.Figure()
    colors = ['#636EFA',
              '#EF553B',
              '#00CC96',
              '#AB63FA',
              '#FFA15A',
              '#19D3F3',
              '#FF6692',
              '#B6E880',
              '#FF97FF',
              '#FECB52']
    if not contents is None:
        for idx, content in enumerate(contents):
            content_type, content_string = content.split(',')
            datei = base64.b64decode(content_string).decode('cp1251')
            volume, Flow, Duration, Interval, Intervals, Hardwarerevision, Softwareversion, Mesurement_status, df \
                = iterprete_txt_file(datei)
            fig_new = px.line(df, x=x_paramerter, y=y_parameter, labels=filename[idx]
                              ).update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)'
            )
            fig_new.update_traces(line_color=colors[idx])
            fig = go.Figure(data=fig.data + fig_new.data).update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                xaxis=dict(
                    title=x_paramerter
                ),
                yaxis=dict(
                    title=y_parameter
                )
            )
            fig.data[idx].name = filename[idx]
            fig.data[idx].showlegend = True
        return fig
    else:
        return fig


@app.callback(
    Output("graph_3", "figure"),
    [Input("upload", "contents"),
     Input("upload", "filename"),
     Input('y_Achse_3', 'value'),
     Input('x_Achse_3', 'value')
     ]
)
def draw_graph_3(contents, filename, y_parameter, x_paramerter):
    time.sleep(1)
    fig = go.Figure()
    colors = ['#636EFA',
              '#EF553B',
              '#00CC96',
              '#AB63FA',
              '#FFA15A',
              '#19D3F3',
              '#FF6692',
              '#B6E880',
              '#FF97FF',
              '#FECB52']
    if not contents is None:
        for idx, content in enumerate(contents):
            content_type, content_string = content.split(',')
            datei = base64.b64decode(content_string).decode('cp1251')
            volume, Flow, Duration, Interval, Intervals, Hardwarerevision, Softwareversion, Mesurement_status, df \
                = iterprete_txt_file(datei)
            fig_new = px.line(df, x=x_paramerter, y=y_parameter, labels=filename[idx]
                              ).update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)'
            )
            fig_new.update_traces(line_color=colors[idx])
            fig = go.Figure(data=fig.data + fig_new.data).update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                xaxis=dict(
                    title=x_paramerter
                ),
                yaxis=dict(
                    title=y_parameter
                )
            )
            fig.data[idx].name = filename[idx]
            fig.data[idx].showlegend = True
        return fig
    else:
        return fig


if __name__ == "__main__":
    app.run_server(debug=True)
