"""
figures.py

Builds Plotly figures for the MH-AI Governance Dashboard.

Functions:
-make_choropleth: US State choropleth map - EOC enacted index
-make_scatter: performative vs protective scatterplot
-make_gap_bar: proposed vs enacted EoC coverage by state
-make_tag_coverage: EoC tag presence across enacted bills

"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def make_choropleth(df: pd.DataFrame) -> go.Figure:
    """""
    US State choropleth colored by EOC enacted index.

    Design call: uses eoc_enacted_index instead of eox_index.
    Enacted bills represent ACTUAL governance, IE protections delivered.
    PRoposed bills represent legislative intent, IE protection promised.
    This map debuts productive, qualitative legislation that became law,
    not the perception of productivity via volume.

    Args: 
    df: DataFrame with state-level indices from index.compute_state_index()

    Returns: Plotly Figure object

    """""
    fig = px.choropleth(
        df,
        locations="state",
        locationmode="USA-states",
        color="eoc_enacted_index",
        scope="usa",
        hover_name="state_name",
        hover_data={
            "state": False,
            "eoc_enacted_index": ":.1f",
            "eoc_index": ":.1f",
            "bill_count": True,
            "enacted_count": True,
            "enacted_pct": ":.1f",
            "eoc_tags_missing": True,
        },
        color_continuous_scale=[
            [0.0, "#f7f7f7"],
            [0.25, "#c6dbef"],
            [0.5,  "#6baed6"],
            [0.75, "#2171b5"],
            [1.0,  "#084594"],
        ],
        labels={
            "eoc_enacted_index": "EoC Enacted Index",
            "eoc_index": "EoC Proposed Index",
            "bill_count": "Total bills",
            "enacted_count": "Enacted bills",
            "enacted_pct": "% enacted",
            "eoc_tags_missing": "Missing protections",
        },
    )

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_colorbar={
            "title": "EoC<br>Enacted<br>Index",
            "thickness": 12,
            "len": 0.6,
        },
        geo={"bgcolor": "rgba(0,0,0,0)"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "system-ui", "size": 11},
    )

    return fig

if __name__ == "__main__":
    from mhai.fetch import fetch_bills
    from mhai.index import compute_state_index

    df = fetch_bills()
    idx = compute_state_index(df)
    fig = make_choropleth(idx)
    fig.show()