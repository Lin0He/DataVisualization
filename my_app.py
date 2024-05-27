from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/Lin0He/DataVisualization/master/psd_coffee.csv')

# Aggregate production data by country
production_by_country = df.groupby("Country")["Production"].sum().reset_index()
import_by_country = df.groupby("Country")["Imports"].sum().reset_index()
export_by_country = df.groupby("Country")["Exports"].sum().reset_index()
consume_by_country = df.groupby("Country")["Domestic Consumption"].sum().reset_index()

production_trend = df.groupby('Year')['Production'].sum().reset_index()
import_trend = df.groupby('Year')['Imports'].sum().reset_index()
export_trend = df.groupby('Year')['Exports'].sum().reset_index()
distribute_trend = df.groupby('Year')['Total Distribution'].sum().reset_index()
supply_trend = df.groupby('Year')['Total Supply'].sum().reset_index()

# Sort and select top 5 production countries
top_production_countries = production_by_country.sort_values(by="Production", ascending=False).head(5)
top_import_countries = import_by_country.sort_values(by="Imports", ascending=False).head(5)
top_export_countries = export_by_country.sort_values(by="Exports", ascending=False).head(5)
top_consume_countries = consume_by_country.sort_values(by="Domestic Consumption", ascending=False).head(5)



# Create the bar chart using Plotly Express
fig1 = px.bar(top_production_countries, x="Country", y="Production")
fig2 = px.bar(top_import_countries, x="Country", y="Imports")
fig3 = px.bar(top_export_countries, x="Country", y="Exports")
fig4 = px.bar(top_consume_countries, x="Country", y="Domestic Consumption")

# Create annual sum data by year
fig5 = px.line(production_trend, x = "Year", y = "Production")
fig6 = px.line(import_trend, x = "Year", y = "Imports")
fig7 = px.line(export_trend, x = "Year", y = "Exports")
fig8 = px.line(distribute_trend, x = "Year", y = "Total Distribution")
fig9 = px.line(supply_trend, x = "Year", y = "Total Supply")

app = Dash(__name__)
server = app.server
app.layout = [

    html.H1(children='Coffee Data Analysis', style={'textAlign':'center'}),
    
    html.Div([
        html.H2(children='World Trends Map', style={'textAlign':'left'}),
        html.Div([
            dcc.Dropdown(['Arabica Production','Bean Exports','Bean Imports','Beginning Stocks','Domestic Consumption','Ending Stocks','Exports','Imports','Other Production','Production','Roast & Ground Exports','Roast & Ground Imports','Robusta Production','"Rst,Ground Dom. Consum"','Soluble Dom. Cons.','Soluble Exports','Soluble Imports','Total Distribution','Total Supply'], 'Total Supply', id='indicate_selection0'),
        ]),
            dcc.Graph(id='indicator_map', style={'width': '100vh', 'height': '100vh', 'display': 'inline-block'}),
    ]),
    
    html.Div([
        html.H2(children='All Data For Coffee Trade Table', style={'textAlign':'left'}),
        html.Div([
            dcc.Dropdown(df.Country.unique(), 'Australia', id='country_value'),
        ],style={'width': '26%', 'display': 'inline-block'}), 
        
        html.Div([
            dcc.Dropdown(['Arabica Production','Bean Exports','Bean Imports','Beginning Stocks','Domestic Consumption','Ending Stocks','Exports','Imports','Other Production','Production','Roast & Ground Exports','Roast & Ground Imports','Robusta Production','"Rst,Ground Dom. Consum"','Soluble Dom. Cons.','Soluble Exports','Soluble Imports','Total Distribution','Total Supply'], 'Total Supply', id='indicate_selection'),
         ],style={'width': '72%', 'float': 'right', 'display': 'inline-block'}), 
        dcc.Graph(id='indicator_graphic'),
    ]),
    
    html.Div([
        html.H2(children='Top indicators', style={'textAlign': 'left'}),
        html.Div([
            html.H3(children='Top Production Countries/Regions', style={'textAlign': 'left'}),
            html.Div([
                dcc.Graph(id='TopProductionCountries', figure=fig1)
            ]),
            html.H3(children='Top Import Countries/Regions', style={'textAlign': 'left'}),
            html.Div([
                dcc.Graph(id='TopImportCountries', figure = fig2)
            ]),
            html.H3(children='Top Export Countries/Regions', style={'textAlign': 'left'}),
            html.Div([
                dcc.Graph(id='TopExportCountries', figure = fig3)
            ]),
            html.H3(children='Top Domestics Consumption Countries/Regions', style={'textAlign': 'left'}),
            html.Div([
                dcc.Graph(id='TopDomesticsConsumptionCountries', figure = fig4)
            ]),
            
            html.H3(children='Global Coffee Production Trends', style={'textAlign': 'left'}),
            html.Div([
                dcc.Graph(id='GlobalCoffeeProductionTrends', figure = fig5)
            ]),
            html.H3(children='Global Coffee Import Trends', style={'textAlign': 'left'}),
            html.Div([
                 dcc.Graph(id='GlobalCoffeeImportTrends', figure = fig6)
            ]),
            html.H3(children='Global Coffee Export Trends', style={'textAlign': 'left'}),
            html.Div([
                 dcc.Graph(id='Global Coffee Export Trends', figure = fig7)
            ]),
            html.H3(children='Global Coffee Total Distribution Trend', style={'textAlign': 'left'}),
            html.Div([
                 dcc.Graph(id='Global Coffee Total Distribution Trend', figure = fig8)
            ]),
            html.H3(children='Global Coffee Total Supply Trend', style={'textAlign': 'left'}),
            html.Div([
                 dcc.Graph(id='Global Coffee Total Supply Trend', figure = fig9)
            ]),
        ])
    ])
]

# Create Map


@callback(
    Output('indicator_graphic', 'figure'),
    Output('indicator_map', 'figure'),
    Input('country_value', 'value'),
    Input('indicate_selection', 'value'),
    Input('indicate_selection0', 'value'),
)

def update_graph(country_value, indicate_selection, indicate_selection0):
    dff = df[df["Country"] == country_value]
    fig = px.line(x=dff['Year'],
                     y=dff[indicate_selection], 
                      )
    
    fig0 = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color=indicate_selection0,
    animation_frame="Year",
    color_continuous_scale="GnBu"  )
    return fig, fig0

if __name__ == '__main__':
    app.run(debug=True)
