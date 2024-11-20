from dash import Input, Output
from components.charts import create_chart
import plotly.graph_objects as go
import pandas as pd

def register_callbacks(app, data):
    # Callback az Országos fülhöz
    @app.callback(
        Output('orszagos-chart', 'figure'),
        [
            Input('orszagos-columns-selector', 'value'),
            Input('orszagos-income-type-selector', 'value'),
            Input('orszagos-chart-type-selector', 'value')
        ]
    )
    def update_orszagos_chart(selected_columns, selected_income_types, selected_chart_types):
        # Ha nincs kiválasztva semmi, adjunk vissza üres diagramot
        if not selected_columns or not selected_income_types or not selected_chart_types:
            return go.Figure()

        # Normál diagram generálása
        return create_chart(data, selected_columns, selected_income_types, selected_chart_types)

    # Callback a Régiók szerint fülhöz
    @app.callback(
        Output('regions-chart', 'figure'),
        [
            Input('regions-columns-selector', 'value'),
            Input('regions-income-type-selector', 'value'),
            Input('regions-chart-type-selector', 'value')
        ]
    )
    def update_regions_chart(selected_columns, selected_income_types, selected_chart_types):
        # Ha nincs kiválasztva semmi, adjunk vissza üres diagramot
        if not selected_columns or not selected_income_types or not selected_chart_types:
            return go.Figure()

        # Csak a "Régiók szerint" oszlopokat szűrjük
        filtered_data = data[[col for col in data.columns if 'Régiók szerint' in col or col in ['Év', 'Jövedelem_típus']]]
        return create_chart(filtered_data, selected_columns, selected_income_types, selected_chart_types)

    # Callback a Települések típusa szerint fülhöz
    @app.callback(
        Output('settlements-chart', 'figure'),
        [
            Input('settlements-columns-selector', 'value'),
            Input('settlements-income-type-selector', 'value'),
            Input('settlements-chart-type-selector', 'value')
        ]
    )
    def update_settlements_chart(selected_columns, selected_income_types, selected_chart_types):
        # Ha nincs kiválasztva semmi, adjunk vissza üres diagramot
        if not selected_columns or not selected_income_types or not selected_chart_types:
            return go.Figure()

        # Csak a "Települések típusa szerint" oszlopokat szűrjük
        filtered_data = data[[col for col in data.columns if 'Települések típusa szerint' in col or col in ['Év', 'Jövedelem_típus']]]
        return create_chart(filtered_data, selected_columns, selected_income_types, selected_chart_types)

    # Callback az Összesített fülhöz
    @app.callback(
        Output('all-chart', 'figure'),
        [
            Input('all-columns-selector', 'value'),
            Input('all-income-type-selector', 'value'),
            Input('all-chart-type-selector', 'value')
        ]
    )
    def update_all_chart(selected_columns, selected_income_types, selected_chart_types):
        # Ha nincs kiválasztva semmi, adjunk vissza üres diagramot
        if not selected_columns or not selected_income_types or not selected_chart_types:
            return go.Figure()

        # Teljes adatot használunk az összesített grafikonhoz
        return create_chart(data, selected_columns, selected_income_types, selected_chart_types)
