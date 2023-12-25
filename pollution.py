from dash import Dash, dcc, Output, Input  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd                        # pip install pandas

# incorporate data into app
# Source - https://www.cdc.gov/nchs/pressroom/stats_of_the_states.htm
df = pd.read_csv("pollution_data.csv")
df['text'] = "State: " + df['State']

# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
mytitle = dcc.Markdown(children='# Pollution Dashboard', style={'textAlign': 'center', 'fontSize': '28px'})
mygraph = dcc.Graph(id="graph")
dropdown = dcc.Dropdown(
    options=df.columns.values[[12,17,22,27,32,47,57,62,67]],
    value='o3_median',  # initial value displayed when page first loads
    clearable=False,
    style={'width': '300px'}
)

mytitle2 = dcc.Markdown(children='# Population Dashboard', style={'textAlign': 'center', 'fontSize': '28px'})

graph2 = dcc.Graph(id="graph2")
dropdown2 = dcc.Dropdown(
    options=df.columns.values[[4,5]],
    value='Population Staying at Home',  # initial value displayed when page first loads
    clearable=False,
    style={'width': '300px'}
)

states_dropdown = dcc.Dropdown(
    options=[{"label": state, "value": state} for state in df["State"].unique()],
    value=[],  # initial value displayed when page first loads
    multi=True,
    style={'width': '300px'}
)

# Customize your own Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([mytitle], width=12)
    ], justify='center'),
    dbc.Row([
        dbc.Col([dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([dropdown], width=6, className='mb-3')
                ], justify='center')
            ])
        ], className='shadow-sm')], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([mygraph], width=12)
    ]),
    dbc.Row([
        dbc.Col([dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([mytitle2], width=12)
                ]),
                dbc.Row([
                    dbc.Col([dropdown2], width=6, className='mb-3')
                ], justify='center')
            ])
        ], className='shadow-sm')], width=6)
    ], justify='center'),

    dbc.Row([
        dbc.Col([dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([states_dropdown], width=6, className='mb-3')
                ], justify='center')
            ])
        ], className='shadow-sm')], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([graph2], width=12)
    ], className='mb-3'),

], fluid=True, style={'padding': '20px'})


# Callbacks allow components to interact
@app.callback(
    Output("graph", "figure"),
    Output(mytitle, 'children'),
    Input(dropdown, 'value')
)
def update_graph(column_name):  # function arguments come from the component property of the Input
    fig = px.choropleth(
        data_frame=df,
        locations=df['State'],
        locationmode="USA-states",
        scope="usa",
        height=600,
        color=column_name,
        color_continuous_scale= 'darkmint',
        animation_frame='Date'
    )
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title=column_name,
        margin={'l': 20, 'r': 20, 't': 60, 'b': 20}
    )
    return fig, '# ' + column_name + ' per State' # returned objects are assigned to the component property of theOutput

# Callbacks allow components to interact
@app.callback(
    Output("graph2", "figure"),
    Output(mytitle2, 'children'),
    Input(dropdown2, 'value'),
    Input(states_dropdown, 'value')
)
def update_graph2(column_name, selected_states):  # function arguments come from the component property of the Input
    filtered_df = df[df["State"].isin(selected_states)]
    fig = go.Figure()
    for state in filtered_df["State"].unique():
        state_df = filtered_df[filtered_df['State'] == state]
        fig.add_trace(go.Scatter(x=state_df['Date'], y=state_df[column_name], mode='lines', name=state))

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title=column_name,
        margin={'l': 20, 'r': 20, 't': 60, 'b': 20}
    )
    return fig, '# ' + column_name + ' per State' # returned objects are assigned to the component property of the Output


# Run app
if __name__ == '__main__':
    app.run_server(debug=True, port=8054)
