import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Load data
df = pd.read_csv('prompt_comparison_report.csv')

# Load prompts
with open('prompts.txt', 'r') as f:
    default_prompt = f.readline()
    new_prompt = f.readline()

app.layout = html.Div([
    dbc.Container([
        html.H1("Evaluation Comparison Report", className="my-4"),
        
        # Filters
        dbc.Row([
            dbc.Col([
                html.Label("Filter by Score Range:"),
                dcc.RangeSlider(
                    id='score-slider',
                    min=0,
                    max=10,
                    value=[0, 10],
                    marks={i: str(i) for i in range(11)}
                )
            ], width=6)
        ], className="mb-4"),
        
        # Prompts Display
        dbc.Button("Show Prompts", id="prompt-button", className="mb-3"),
        dbc.Collapse([
            dbc.Card([
                dbc.CardHeader("Evaluation Prompts"),
                dbc.CardBody([
                    html.H5("Default Prompt"),
                    html.Pre(default_prompt),
                    html.H5("New Prompt"),
                    html.Pre(new_prompt)
                ])
            ])
        ], id="prompt-collapse"),
        
        # Results Table
        html.Div(id='filtered-table')
    ])
])

@app.callback(
    Output('filtered-table', 'children'),
    Input('score-slider', 'value')
)
def update_table(score_range):
    filtered_df = df[
        (df['default_score'].between(score_range[0], score_range[1])) |
        (df['new_score'].between(score_range[0], score_range[1]))
    ]
    
    return dbc.Table.from_dataframe(
        filtered_df,
        striped=True,
        bordered=True,
        hover=True,
        responsive=True
    )

@app.callback(
    Output("prompt-collapse", "is_open"),
    [Input("prompt-button", "n_clicks")],
    [dash.State("prompt-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True)
