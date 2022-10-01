from ast import Div
from dash import html, dash_table

table_block_style = {
    "height": "100%",
    "width": "50%",
    "padding": "15px",
    "margin-left": "auto",
    "margin-right": "auto",
}


def render_stats_table(stats_data: dict[str, list]) -> Div:
    return html.Div(
        [
            html.H1("Pressure Stats"),
            html.Div(
                children=[
                    dash_table.DataTable(
                        id="diastolic_table",
                        columns=(
                            {"name": "Diastolic", "id": "name"},
                            {"name": "[mmHg]", "id": "value"},
                        ),
                        data=stats_data["data_up"],
                    ),
                    dash_table.DataTable(
                        id="systolic_table",
                        columns=(
                            {"name": " Systolic", "id": "name"},
                            {"name": "[mmHg]", "id": "value"},
                        ),
                        data=stats_data["data_down"],
                    ),
                    dash_table.DataTable(
                        id="pulse_table",
                        columns=(
                            {"name": "   Pulse", "id": "name"},
                            {"name": "[bpm]", "id": "value"},
                        ),
                        data=stats_data["data_pulse"],
                    ),
                ],
                className="block_2",
                style=table_block_style,
            ),
        ]
    )
