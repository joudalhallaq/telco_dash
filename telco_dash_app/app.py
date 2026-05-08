import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df.dropna(inplace=True)

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Telco Customer Churn Dashboard"),

    html.Label("Select Contract Type:"),

    dcc.Dropdown(
        id="contract_filter",
        options=[{"label": c, "value": c} for c in df["Contract"].unique()],
        value=df["Contract"].unique()[0]
    ),

    dcc.Graph(id="churn_chart"),
    dcc.Graph(id="charges_chart")
])

@app.callback(
    [Output("churn_chart", "figure"),
     Output("charges_chart", "figure")],
    Input("contract_filter", "value")
)
def update_charts(selected_contract):
    filtered_df = df[df["Contract"] == selected_contract]

    fig1 = px.histogram(filtered_df, x="Churn", color="Churn")

    fig2 = px.scatter(
        filtered_df,
        x="MonthlyCharges",
        y="TotalCharges",
        color="Churn",
        size="tenure"
    )

    return fig1, fig2

if __name__ == "__main__":
    app.run(debug=True)