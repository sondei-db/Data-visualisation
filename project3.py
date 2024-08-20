import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import webbrowser

data = pd.read_csv('covid_worldwide.csv')

data['Covid Cases Percentage'] = (data['Total Cases'] / data['Population']) * 100
data['Covid Deaths Percentage'] = (data['Total Deaths'] / data['Total Cases']) * 100
data['Covid Recovered Percentage'] = (data['Total Recovered'] / data['Total Cases']) * 100

color_range = {
    'Covid Cases Percentage': [0, 100],
    'Covid Deaths Percentage': [0, 30],
    'Covid Recovered Percentage': [0, 100],
}

custom_color_scale = {
    'Covid Cases Percentage': [
        [0.0, '#FFBA08'],
        [0.02, '#FAA307'],
        [0.04, '#F48C06'],
        [0.06, '#E85D04'],
        [0.1, '#dc2f02'],
        [0.2, '#d00000'],
        [0.4, '#9d0208'],
        [0.6, '#6a040f'],
        [0.9, '#370617'],
        [1.0, '#03071e']
    ],
    'Covid Deaths Percentage': [
        [0.0, '#ffba08'],
        [0.02, '#faa307'],
        [0.05, '#f48c06'],
        [0.1, '#f48c06'],
        [0.2, '#dc2f02'],
        [0.3, '#d00000'],
        [0.4, '#9d0208'],
        [0.5, '#6a040f'],
        [0.7, '#370617'],
        [1.0, '#03071e']
    ],
    'Covid Recovered Percentage': [
        [0.0, '#252422'],
        [0.02, '#233d4d'],
        [0.04, '#132a13'],
        [0.06, '#31572c'],
        [0.1, '#4f772d'],
        [0.2, '#004b23'],
        [0.4, '#007200'],
        [0.6, '#008000'],
        [0.9, '#38b000'],
        [1.0, '#70e000']
    ]
}

columns = ['Covid Cases Percentage', 'Covid Deaths Percentage', 'Covid Recovered Percentage']

mean_cases_percentage = data['Covid Cases Percentage'].mean()
min_cases_percentage = data['Covid Cases Percentage'].min()
max_cases_percentage = data['Covid Cases Percentage'].max()
min_country = data.loc[data['Covid Cases Percentage'].idxmin(), 'Country']
max_country = data.loc[data['Covid Cases Percentage'].idxmax(), 'Country']

def calculate_custom_statistics():
    total_cases = data['Total Cases'].sum()
    total_deaths = data['Total Deaths'].sum()
    total_recovered = data['Total Recovered'].sum()
    return total_cases, total_deaths, total_recovered

total_cases, total_deaths, total_recovered = calculate_custom_statistics()

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1("COVID-19 Dashboard", style={'text-align': 'center'}),
        dcc.Tabs(
            id="tabs",
            value="map",
            children=[
                dcc.Tab(label="Details", value="map", children=[
                    html.Div(style={'margin-bottom': '40px'}),  # Add this line for spacing
                    html.Div(
                        [
                            html.H3("General Covid Cases", style={'text-align': 'center','fontSize': '26px', 'margin-top': '10px'}),
                            html.Div(
                                [ 
                                    html.P(f"Average value: {mean_cases_percentage:.2f}%", style={'margin-right': '20px', 'fontSize': '20px'}),
                                    html.P(f"Lowest value: {min_country} - {min_cases_percentage:.2f}%", style={'margin-right': '20px', 'fontSize': '20px'}),
                                    html.P(f"Highest value:  {max_country} - {max_cases_percentage:.2f}%", style={'margin-right': '20px', 'fontSize': '20px'}),
                                ],
                                style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '20px'},
                            ),
                            dcc.Dropdown(
                            id="country-dropdown",
                            options=[{"label": country, "value": country} for country in data['Country']],
                            placeholder="Select a country",
                            clearable=True,
                            ),
                            html.H3( 
                                    id="country-statistics-title", 
                                    style={'text-align': 'center', 'margin-bottom': '10px', 'fontSize': '24px', 'display': 'none'}),
                            html.Div(id="statistics-output",
                                    style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '10px'}),
                        ],
                    ),
                    html.Div(style={'margin-bottom': '50px'}),  # Add this line for spacing
                    dcc.Dropdown(
                        id="column-dropdown",
                        options=[{"label": col, "value": col} for col in columns],
                        value=columns[0],
                        clearable=False,
                    ),
                    html.Div(id="choropleth-output", style={'display': 'flex', 'justify-content': 'center'}),
                    html.Div(
                        [
                            html.Div(
                                children=[
                                    html.Img(id='image1', src='https://git.wmi.amu.edu.pl/s452627/Wykresiki_z_Wizualizacji/raw/commit/d63e3999b6292648a497f6bea8f2ab5eb03d994b/Rplot16.png', style={'width': '1920px', 'height': '856px', 'cursor': 'pointer'}),
                                ],
                                style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'margin-bottom': '10px'}
                            ),
                            html.Div(
                                children=[
                                    html.Img(id='image2', src='https://git.wmi.amu.edu.pl/s452627/Wykresiki_z_Wizualizacji/raw/commit/fd95973a9e522a95c6fa0c99ad77f2c125818b52/Rplot18.png', style={'width': '1920px', 'height': '908px', 'cursor': 'pointer'}),
                                ],
                                style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'margin-bottom': '10px', 'margin-left': '100px'}
                            ),
                            # Add more html.Div elements for additional images
                        ],
   
                    ),         
                ]),
                dcc.Tab(label="Dataset", value="table", children=[
                    html.Div(id="table-output"),
                ]),
            ],
        ),
    ]
)


@app.callback(
    Output("statistics-output", "children"),
    Output("country-statistics-title", "style"),
    Output("country-statistics-title", "children"),
    Input("country-dropdown", "value"),
)
def update_statistics(selected_country):
    if selected_country:
        country_data = data[data['Country'] == selected_country]
        country_statistics = [
            html.P(f"Total Cases: {country_data['Total Cases'].values[0]}", style={'margin-right': '20px', 'fontSize': '20px'}),
            html.P(f"Total Deaths: {country_data['Total Deaths'].values[0]}", style={'margin-right': '20px', 'fontSize': '20px'}),
            html.P(f"Total Recovered: {country_data['Total Recovered'].values[0]}", style={'fontSize': '20px'}),
        ]
        title = f"{selected_country} Statistics"
        title_style = {'textAlign': 'center', 'marginBottom': '10px', 'fontSize': '24px'}
    else:
        country_statistics = []
        title = None
        title_style = {'display': 'none'}

    return country_statistics, title_style, title

@app.callback(
    Output("choropleth-output", "children"),
    Input("column-dropdown", "value"),
)
def update_choropleth(column):
    fig = px.choropleth(
        data,
        locations='AlphaCode',
        color=column,
        hover_data={'Country': True, column: True, 'AlphaCode': False},
        color_continuous_scale=custom_color_scale[column],
        range_color=color_range[column],
    )
    fig.update_layout(height=800, width=1400)
    fig.update_layout(legend_title_text='', title=column, title_font={'size': 24}, title_x=0.5, title_y=0.95)
    fig.update_layout(showlegend=False)
    fig.update_traces(colorbar_title=None)
    fig.update_layout(
        coloraxis_colorbar=dict(
            title='',
            ticktext=[]
        )
    )

    return dcc.Graph(figure=fig)

@app.callback(
    Output("country-dropdown", "value"),
    Input("tabs", "value")
)
def reset_country_dropdown(tab):
    if tab == "table":
        return None  # Reset the selected country value
    return dash.no_update

@app.callback(
    Output("table-output", "children"),
    Input("tabs", "value"),
    Input("country-dropdown", "value"),
)
def update_table(tab, selected_country):
    if tab == "table":
        columns_to_display = [col for col in data.columns if col != 'Serial Number']
        table_data = data  # Use the entire dataset by default

        if selected_country:
            table_data = data[data['Country'] == selected_country]
            selected_country = None  # Reset the selected country

        table = html.Table(
            [html.Tr([html.Th(col) for col in columns_to_display])] +
            [html.Tr([html.Td(table_data.iloc[i][col]) for col in columns_to_display]) for i in range(len(table_data))]
        )
        return table

    return None

if __name__ == "__main__":
    app.run_server(debug=True)
