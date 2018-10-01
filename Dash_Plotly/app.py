import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from plotly import tools
from dash.dependencies import Input, Output
from categoryplot import dfTitanic, getPlot
import numpy as np

app = dash.Dash() # make python obj with Dash() method

color_set = {
    'survived': ['#ff3fd8','#4290ff'],
    'sex': ['#32fc7c','#ed2828'],
    'class': ['#0059a3','#f2e200'],
    'embark': ['#ff8800','#ddff00'],
    'who': ['#0059a3','#f2e200'],
    'outlier': ['#0059a3','#f2e200']
}

app.title = 'Purwadhika Dash Plotly'; # set web title

# function to generate HTML Table
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col,className='table_dataset') for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col],className='table_dataset') for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
        ,className='table_dataset'
    )

#the layout/content
app.layout = html.Div(children=[
    dcc.Tabs(id="tabs", value='tab-1', 
        style={
            'fontFamily': 'system-ui'
        },
        content_style={
            'fontFamily': 'Arial',
            'borderLeft': '1px solid #d6d6d6',
            'borderRight': '1px solid #d6d6d6',
            'borderBottom': '1px solid #d6d6d6',
            'padding': '44px'
        }, 
        children=[
            dcc.Tab(label='Titanic Data Set', value='tab-1', children=[
                html.Div([
                    html.H1('Titanic Data Set'),
                    html.Div(children=[], id='tablefare')
                    ])
                ]),
            dcc.Tab(label='Categorical Plot', value='tab-2', children=[
                html.Div([
                    html.H1('Categorical Plot Titanic Data Set'),
                    dcc.RangeSlider(
                        id='fare-range-slider',
                        min=min(dfTitanic['fare']),
                        max=max(dfTitanic['fare']),
                        step = 1,
                        value=[min(dfTitanic['fare']), max(dfTitanic['fare'])]
                    ),
                    html.Table([
                        html.Tr([
                            html.Td([
                                html.P('Jenis : '),
                                dcc.Dropdown(
                                    id='ddl-jenis-plot-category',
                                    options=[{'label': 'Bar', 'value': 'bar'},
                                            {'label': 'Violin', 'value': 'violin'},
                                            {'label': 'Box', 'value': 'box'}],
                                    value='bar'
                                )
                            ]),
                            html.Td([
                                html.P('X Axis : '),
                                dcc.Dropdown(
                                    id='ddl-x-plot-category',
                                    options=[{'label': 'Survived', 'value': 'survived'},
                                            {'label': 'Sex', 'value': 'sex'},
                                            {'label': 'Ticket Class', 'value': 'class'},
                                            {'label': 'Embark Town', 'value': 'embark'},
                                            {'label': 'Who', 'value': 'who'},
                                            {'label': 'Outlier', 'value': 'outlier'}],
                                    value='who'
                                )
                            ])
                        ])
                    ], style={ 'width' : '700px', 'margin': '0 auto'}),
                    dcc.Graph(
                        id='categoricalPlot',
                        figure={
                            'data': []
                        }
                    )
                ])
            ])
    ])
], 
style={
    'maxWidth': '1000px',
    'margin': '0 auto'
});

@app.callback(
    Output('tablefare', 'children'),
    [Input('fare-range-slider','value')]
)
def update_tb_table(tbrangeslider):
    filterdfTitanic=dfTitanic[(dfTitanic['fare']>=tbrangeslider[0]) & (dfTitanic['fare']<=tbrangeslider[1])]
    filterdfTitanic.sort_values(by=['fare'], inplace=True)
    return [
        html.P('Total row: ' + str(len(filterdfTitanic))),
        dcc.Graph(
            id='hehe',
            figure = {
                'data':[
            go.Table(
                header=dict(
                    values=['<b>' + col + '</b>' for col in dfTitanic.columns],
                    font=dict(size=18),
                    height=30,
                    fill=dict(color='#a1c3d1')
                ),
                cells=dict(
                    values=[dfTitanic[col] for col in dfTitanic.columns],
                    font=dict(size=16),
                    height=30,
                    fill=dict(color='#EDFAFF'),
                    align=['right']
                )
            )
            ],
            'layout' : dict(height=500, margin={'l': 40, 'b': 40, 't': 10, 'r': 10})
        }
        )
    ]

@app.callback(
    Output('categoricalPlot', 'figure'),
    [Input('ddl-jenis-plot-category', 'value'),
    Input('ddl-x-plot-category', 'value')])
def update_category_graph(ddljeniscategory, ddlxcategory):
    return {
            'data': getPlot(ddljeniscategory,ddlxcategory),
            'layout': go.Layout(
                xaxis={'title': ddlxcategory.capitalize()}, yaxis={'title': 'US$'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1.2}, hovermode='closest',
                boxmode='group',violinmode='group'
                # plot_bgcolor= 'black', paper_bgcolor= 'black',
            )
    };

if __name__ == '__main__':
    # run server on port 1997
    # debug=True for auto restart if code edited
    app.run_server(debug=True, port=2000) 