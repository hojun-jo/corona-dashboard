
from click import style
from dash import Dash, html, dcc
from matplotlib.pyplot import figure
import plotly.express as px
from data import countries_df, totals_df, dropdown_options, make_global_df, make_country_df
from builders import make_table
from dash.dependencies import Input, Output

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap"]

app = Dash(__name__, external_stylesheets = stylesheets)

bubble_map = px.scatter_geo(countries_df, 
                     hover_name="Country_Region",
                     color="Confirmed", 
                     locations="Country_Region",
                     locationmode="country names", 
                     hover_data={"Country_Region":False,
                                  "Confirmed":":,",
                                  "Recovered":":,",
                                  "Deaths":":,"},
                     size="Confirmed",
                     size_max=40,
                     template="plotly_dark",
                     color_continuous_scale=px.colors.sequential.Oryel,
                     title="Confirmed By Country"
                    )
bubble_map.update_layout(
    margin=dict(l=0, r=0, t=50, b=0), 
    coloraxis_colorbar=dict(xanchor="left", x=0)
)


bars_graph = px.bar(totals_df, 
             x="condition", 
             y="count", 
             template="plotly_dark", 
             title="Total Global Cases",
            hover_data={"count": ":,"},
            labels={
                "condition":"Condition",
                "count":"Count",
                "color":"Condition"
            },
)
bars_graph.update_traces(marker_color=["#e74c3c", "#8e44ad", "#27ae60"])


app.layout = html.Div(
    style = {
        "minHeight": "100vh", 
        "backgroundColor": "#111111", 
        "color": "white",
        "fontFamily": "Open Sans, sans-serif"
    },
    children = [
        html.Header(
            style = {
                "textAlign": "center",
                "paddingTop": "50px",
                "marginBottom": 100
            },
            children = [html.H1("Corona Dashboard", style = {"fontSize": 40})]
        ),
        html.Div(
            style = {
                "display": "grid",
                "gridTemplateColumns": "repeat(4, 1fr)",
                "gap": 50
            },
            children = [
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[
                        dcc.Graph(figure=bubble_map)
                    ]
                ),
                html.Div(
                    children=[
                        make_table(countries_df)
                    ]
                )
            ]
        ),
        html.Div(
            style = {
                        "display": "grid",
                        "gridTemplateColumns": "repeat(4, 1fr)",
                        "gap": 50
            },
            children = [
                html.Div(
                    children=[
                        dcc.Graph(figure=bars_graph)
                    ]
                ),
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[
                        dcc.Dropdown(
                            style = {
                                "width": 320,
                                "margin": "0 auto",
                                "color": "#111111"
                            },
                            placeholder = "Select a Country",
                            id="country",
                            options=[
                                {"label": country, "value": country} for country in dropdown_options
                            ]
                        ),
                        dcc.Graph(id="country_graph")
                    ]
                )
            ]
        )
    ], 
)


@app.callback(
    Output("country_graph", "figure"),
    [
        Input("country", "value")
    ]
)
def update_hello(value):
    if value:
        df = make_country_df(value)
    else:
        df = make_global_df()
    fig = px.line(
        df, 
        x = "date", 
        y = ["confirmed", "deaths", "recovered"],
        template = "plotly_dark",
        labels = {"value": "Cases", 
                "variable": "Condition", 
                "date": "Date"
        },
        hover_data = {
            "value": ":,",
            "variable": False,
            "date": False
        }
    )  
    fig.update_xaxes(rangeslider_visible=True)
    fig["data"][0]["line"]["color"] = "#e74c3c"
    fig["data"][1]["line"]["color"] = "#8e44ad"
    fig["data"][2]["line"]["color"] = "#27ae60"

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)