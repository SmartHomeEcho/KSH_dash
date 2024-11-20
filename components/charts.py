import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import pandas as pd

def create_chart(data, selected_columns, income_types, chart_types):
    # Ha nincs kiválasztva semmi, adjunk vissza üres diagramot
    if not selected_columns or not income_types or not chart_types:
        return go.Figure()  # Üres diagram visszaadása

    fig = go.Figure()

    for income_type in income_types:
        for column in selected_columns:
            # Szűrés az adott jövedelemtípusra és oszlopra
            filtered_data = data[data['Jövedelem_típus'] == income_type] if 'Jövedelem_típus' in data.columns else pd.DataFrame()

            # Ellenőrizzük, hogy van-e adat
            if filtered_data.empty or column not in filtered_data.columns:
                continue

            # Csak érvényes adatok megjelenítése
            filtered_data_nonan = filtered_data[['Év', column]].dropna()

            if filtered_data_nonan.empty:
                continue

            # Grafikon típusok feldolgozása
            for chart_type in chart_types:
                if chart_type == 'Vonal':
                    fig.add_trace(go.Scatter(
                        x=filtered_data_nonan['Év'],
                        y=filtered_data_nonan[column],
                        mode='lines',
                        name=f"{income_type} - {column}",
                        showlegend=True
                    ))
                elif chart_type == 'Pont':
                    fig.add_trace(go.Scatter(
                        x=filtered_data_nonan['Év'],
                        y=filtered_data_nonan[column],
                        mode='markers',
                        name=f"{income_type} - {column}",
                        showlegend=True
                    ))

    # Lineáris regresszió hozzáadása
    if 'Lineáris regresszió' in chart_types:
        for income_type in income_types:
            income_filtered_data = data[data['Jövedelem_típus'] == income_type]
            fig = add_linear_regression_combined(
                fig,
                income_filtered_data,
                x_column='Év',
                y_columns=selected_columns,
                label=income_type
            )

    # Diagram kinézetének frissítése
    fig.update_layout(
        title="Jövedelem Alakulása",
        xaxis_title="Év",
        yaxis_title="Jövedelem (Ft)",
        legend=dict(
            title="Típus",
            orientation="h",
            x=0.5,
            y=-0.2,
            xanchor="center",
            yanchor="top"
        ),
        showlegend=True,
        margin=dict(l=50, r=50, t=50, b=150)  # Extra alsó margó a magyarázat számára
    )
    return fig

def add_linear_regression_combined(fig, filtered_data, x_column, y_columns, label):
    try:
        combined_data = filtered_data[[x_column] + y_columns].dropna()
    except KeyError:
        return fig  # Ha az oszlopok hiányoznak, térjünk vissza az eredeti ábrával

    if combined_data.empty or len(combined_data) < 2:
        return fig  # Nem adunk hozzá regressziót, ha nincs elég adat

    x_values = combined_data[x_column].values.reshape(-1, 1)
    y_values = combined_data[y_columns].mean(axis=1).values

    model = LinearRegression()
    model.fit(x_values, y_values)
    y_pred = model.predict(x_values)

    fig.add_trace(go.Scatter(
        x=combined_data[x_column],
        y=y_pred,
        mode='lines',
        name=f"{label} - Lineáris Regresszió",
        line=dict(dash='dash')
    ))

    return fig
