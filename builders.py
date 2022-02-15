from dash import html


def make_table(df):
    return html.Table(
        style={"display": "block", "marginBottom": 25},
        children=[
            html.Thead(
                children=[
                    html.Tr(
                        children=[
                            html.Th(column_name.replace("_", " ")) for column_name in df.columns
                        ],
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "repeat(4, 1fr)",
                            "fontWeight": "600",
                            "fontSize": 15,
                        },
                    )
                ]
            ),
            html.Tbody(
                style={"maxHeight": "50vh", "display": "block", "overflow": "scroll",},
                children=[
                    html.Tr(
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "repeat(4, 1fr)",
                            "border-top": "1px solid white",
                            "padding": "30px 0px",
                            "gap": 40,
                            "fontSize": 14
                        },
                        children=[
                            html.Td(
                                value_column
                            ) for value_column in value
                        ]
                    ) for value in df.values
                ]
            )
        ]
    )
                    