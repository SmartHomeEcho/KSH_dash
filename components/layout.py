from dash import dcc, html

def create_tab(tab_id, label, column_options, income_type_id, chart_type_id, graph_id):
    return dcc.Tab(
        label=label,
        children=[
            html.Div(
                children=[
                   html.Div(
                children=[
                    
                      html.Div(
                        children=[
                    html.Label("Válassz oszlopokat:"),
                    dcc.Checklist(
                        id=f"{tab_id}-columns-selector",
                        options=[
                            {'label': col, 'value': val} for col, val in column_options
                        ],
                        value=[],
                        style={'margin': '-4px','margin-top':'10px'}
                    ),],
                        className="text-box",
                        ),
                    
                      html.Div(
                children=[
                    html.Label("Válassz jövedelemtípust:"),
                    dcc.Checklist(
                        id=income_type_id,
                        options=[
                            {'label': 'Bruttó', 'value': 'Bruttó jövedelem'},
                            {'label': 'Nettó', 'value': 'Nettó jövedelem'}
                        ],
                        value=['Bruttó jövedelem'],
                        style={'margin': '-4px','margin-top':'10px'}
                    ),],
                
                        className="text-box",),
                    
                      html.Div(
                children=[
                    html.Label("Válassz diagramtípust:"),
                    dcc.Checklist(
                        id=chart_type_id,
                        options=[
                            {'label': 'Vonal', 'value': 'Vonal'},
                            {'label': 'Pont', 'value': 'Pont'},
                            {'label': 'Lineáris regresszió', 'value': 'Lineáris regresszió'}
                        ],
                        value=['Vonal'],
                        style={'margin': '-4px','margin-top':'10px'}
                    ),],
                        className="text-box",),
                ],
                className="check-box",
                    ),
                    dcc.Graph(id=graph_id),
                ],
                className="container",  
                
            ),
        ],
    )


def create_layout(data):
    # Az oszlopok nevének egyszerűsítése
    simplified_columns = [
        (col.split(":")[-1].strip(), col) for col in data.columns if col not in ['Jövedelem_típus', 'Év']
    ]

    tabs = [
        create_tab(
            tab_id="orszagos",
            label="Országos",
            column_options=[('Ország összesen', 'Ország összesen')],
            income_type_id="orszagos-income-type-selector",
            chart_type_id="orszagos-chart-type-selector",
            graph_id="orszagos-chart"
        ),
        create_tab(
            tab_id="regions",
            label="Régiók szerint",
            column_options=[
                (col.split(":")[-1].strip(), col) for col in data.columns if "Régiók szerint" in col
            ],
            income_type_id="regions-income-type-selector",
            chart_type_id="regions-chart-type-selector",
            graph_id="regions-chart"
        ),
        create_tab(
            tab_id="settlements",
            label="Települések típusa szerint",
            column_options=[
                (col.split(":")[-1].strip(), col) for col in data.columns if "Települések típusa szerint" in col
            ],
            income_type_id="settlements-income-type-selector",
            chart_type_id="settlements-chart-type-selector",
            graph_id="settlements-chart"
        ),
        create_tab(
            tab_id="all",
            label="Összesített",
            column_options=simplified_columns,
            income_type_id="all-income-type-selector",
            chart_type_id="all-chart-type-selector",
            graph_id="all-chart"
        )
    ]

    return html.Div([
        dcc.Tabs(tabs)
    ])
