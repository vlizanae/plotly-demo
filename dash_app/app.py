import pandas as pd

from plotly import graph_objs as plgo

import dash
import dash_core_components as dcc
import dash_html_components as html

from dash import dependencies as ddp


data = pd.read_csv('pokemons.csv')
data.type2 = data.type2.fillna(data.type1)

### Figure 1 ###
fig1 = plgo.Figure()

trace = plgo.Histogram2d()
trace.x = data.type2
trace.y = data.type1
trace.colorscale = [
    (0, '#B0FF60'),    # green
    (1/16, '#FFFF60'), # yellow
    (1/4, '#FFB060'),  # orange
    (1, '#FF6060'),    # red
]

fig1.add_trace(trace)

fig1.layout.title = 'Pokemon Heatmap'
fig1.layout.xaxis.title = 'Main type'
fig1.layout.yaxis.title = 'Secondary type'
# fig1.layout.height = 600
# fig1.layout.width = 600
fig1.layout.xaxis.categoryorder = 'category ascending'
fig1.layout.yaxis.categoryorder = 'category ascending'
### Figure 1 ###

### Figure 2 ###
def get_pokescatter(data, types, log):
    fig2 = plgo.Figure()

    trace2 = plgo.Scatter()
    trace2.x = data.weight
    trace2.y = data.height

    trace2.hoverinfo = 'text'
    trace2.text = data.name

    trace2.mode = 'markers'
    trace2.marker.size = 10
    trace2.marker.color = '#60FF60'
    trace2.marker.line.width = 2
    trace2.marker.line.color = '#308030'

    fig2.add_trace(trace2)

    fig2.layout.title = 'Pokemons'
    if len(types) == 2:
        fig2.layout.title = 'Pokemons, {} - {}'.format(*types)

    fig2.layout.xaxis.title = 'weight'
    fig2.layout.yaxis.title = 'height'
    fig2.layout.hovermode = 'closest'

    if log:
        fig2.layout.xaxis.type = 'log'
        fig2.layout.yaxis.type = 'log'
    else:
        fig2.layout.xaxis.rangemode = 'tozero'
        fig2.layout.yaxis.rangemode = 'tozero'

    return fig2
### Figure 2 ###

### Layouts ###
first_layout = html.Div(children = [
    # Plots
    html.Div(children = [

        # Heatmap
        html.Div(children = [
            html.H4(children = 'This is a heatmap.'),
            dcc.Graph(
                id = 'poke-heatmap',
                figure = fig1
            )
        ], className = 'six columns'),

        # Scatter
        html.Div(children = [
            html.H4(children = 'This is a scatterplot.'),
            dcc.Graph(
                id = 'poke-scatter',
            )
        ], className = 'six columns'),

    ], className = 'row')
    # end Plots
])

second_layout = html.Div(children = [
    # Widgets
    html.Div(children = [

        # Sliders
        html.Div(children = [
            # Height slider
            html.H6(children = 'Height range:'),
            dcc.RangeSlider(
                id = 'height-slider',
                min = 0,
                max = data.height.max(),
                step = 1,
                value = [0, data.height.max()],
                marks = {int(i*data.height.max()/9): int(i*data.height.max()/9) for i in range(10)},
            ),
            html.Br(),

            # Weight slider
            html.H6(children = 'Weight range:'),
            dcc.RangeSlider(
                id = 'weight-slider',
                min = 0,
                max = data.weight.max(),
                step = 1,
                value = [0, data.weight.max()],
                marks = {int(i*data.weight.max()/9): int(i*data.weight.max()/9) for i in range(10)},
            )
        ], className = 'six columns'),

        # Log axis
        html.Div(children = [
            html.H6(children = 'Axis mode:'),
            dcc.RadioItems(
                id = 'axis-mode',
                options = [
                    {'label': 'Normal', 'value': False},
                    {'label': 'Logarithmic', 'value': True},
                ],
                value = False,
            )
        ], className = 'six columns'),

    ], className = 'row'),
    # end Widgets

    html.Br(),
    html.Hr(),

    # Plots
    html.Div(children = [

        # Scatter
        html.Div(children = [
            html.H4(children = 'This is another scatterplot.'),
            dcc.Graph(
                id = 'poke-scatter2',
            )
        ], className = 'eight columns, offset-by-two columns'),

    ], className = 'row')
    # end Plots
])
### Layouts ###

## Init ##

app = dash.Dash()

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.config['suppress_callback_exceptions'] = True

## Layout ##

app.layout = html.Div(children = [
    # Header
    dcc.Markdown('''
# **This is Dash**
---
## My Final Dashboard:
    '''),
    # end Header

    dcc.Tabs(
        id = 'tabs',
        value = 'tab1',
        children = [
            dcc.Tab(label='My Dashboard', value='tab1'),
            dcc.Tab(label='My Other Dashboard', value='tab2'),
        ]
    ),
    html.Div(id='tab-content')

], className = 'container')

## Callbacks ##

@app.callback(
    ddp.Output(component_id='tab-content', component_property='children'),
    [ddp.Input(component_id='tabs', component_property='value')]
)
def render_content(tab):
    if tab == 'tab1':
        return first_layout
    if tab == 'tab2':
        return second_layout

@app.callback(
    ddp.Output(component_id='poke-scatter', component_property='figure'),
    [ddp.Input(component_id='poke-heatmap', component_property='clickData')]
)
def filter_scatter(click_data):
    if click_data:
        type1 = click_data['points'][0]['y']
        type2 = click_data['points'][0]['x']
        mask = (data.type1 == type1) & (data.type2 == type2)
        return get_pokescatter(data[mask], [type1, type2], True)
    return get_pokescatter(data, [], True)

@app.callback(
    ddp.Output(component_id='poke-scatter2', component_property='figure'),
    [
        ddp.Input(component_id='height-slider', component_property='value'),
        ddp.Input(component_id='weight-slider', component_property='value'),
        ddp.Input(component_id='axis-mode', component_property='value'),
    ]
)
def widgets_scatter(heights, weights, log):
    mask = (data.height.between(*heights, inclusive=True)) & (data.weight.between(*weights, inclusive=True))
    return get_pokescatter(data[mask], [], log=log)

## Server ##

app.run_server(host='0.0.0.0', port=80)
