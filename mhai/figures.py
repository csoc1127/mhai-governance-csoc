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
from plotly.subplots import make_subplots
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

def make_scatter(df: pd.DataFrame) -> go.Figure:
    """
    Performative vs Protective scatter plot.

    X axis: rai_enacted_index — responsible AI protections actually enacted
    Y axis: eoc_enacted_index — care-based protections actually enacted
    Size: bill_count — legislative volume
    Color: enacted_pct — what percentage actually passed

    Design call: both axes use enacted indices only.
    Proposed coverage excluded; this chart measures governance, not intent.

    The bottom-right cluster is the thesis: states with responsible AI coverage 
    but no care-based protections.

    """
    # only show active states
    dff = df[df["bill_count"] > 0].copy()

    # label the outliers explicitly
    label_states = {"MA", "TX", "IL", "RI", "CA", "CO", "UT", "NY"}
    dff["label"] = dff.apply(
        lambda r: r["state"] if r["state"] in label_states else "", axis=1
    )

    fig = px.scatter(
        dff,
        x="rai_enacted_index",
        y="eoc_enacted_index",
        size="bill_count",
        color="enacted_pct",
        hover_name="state_name",
        text="label",
        hover_data={
            "rai_enacted_index": ":.1f",
            "eoc_enacted_index": ":.1f",
            "bill_count": True,
            "enacted_pct": ":.1f",
            "enacted_count": True,
            "eoc_tags_missing": True,
        },
        color_continuous_scale=[
            [0.0, "#f7f7f7"],
            [0.25, "#c6dbef"],
            [0.5, "#6baed6"],
            [1.0, "#084594"],
        ],
        labels={
            "rai_enacted_index": "Responsible AI Index (enacted)",
            "eoc_enacted_index": "Ethics of Care Index (enacted)",
            "bill_count": "Total bills",
            "enacted_pct": "% enacted",
            "enacted_count": "Enacted bills",
            "eoc_tags_missing": "Missing EoC protections",
        },
        size_max=40,
    )

    fig.update_traces(
        textposition="top center",
        textfont={"size": 11, "color": "#1a1a2e"},
    )

    # quadrant lines
    fig.add_hline(
        y=5.0,
        line_dash="dot",
        line_color="#ccc",
        annotation_text="EoC midpoint",
        annotation_position="right",
        annotation_font_size=10,
    )
    fig.add_vline(
        x=5.0,
        line_dash="dot",
        line_color="#ccc",
        annotation_text="RAI midpoint",
        annotation_position="top",
        annotation_font_size=10,
    )

    fig.update_layout(
        margin={"r": 40, "t": 20, "l": 40, "b": 40},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Georgia, serif", "size": 11},
        coloraxis_colorbar={
            "title": "% enacted",
            "thickness": 12,
            "len": 0.6,
        },
        xaxis={
            "gridcolor": "#f0ede8",
            "range": [-0.5, 11],
            "title": "Responsible AI Index — enacted bills only",
        },
        yaxis={
            "gridcolor": "#f0ede8",
            "range": [-0.5, 11],
            "title": "Ethics of Care Index — enacted bills only",
        },
    )

    return fig


def make_gap_bar(df: pd.DataFrame) -> go.Figure:
    """"
    Side-by-side horizontal bar charts -
    EoC and RAI proposed vs enacted coverage by state

    Left panel: Ethics of Care Index (8 care-based tags)
    Right panel: Responsible AI Index (17 standard regulatory tags)
    
    Panels show proposed vs enacted coverage for each active state.
    Sorted by EoC gap descending, so states with biggest EoC protection
    discrepancy surface to the top.

    Design call: overlay mode where light bar is proposed, dark bar is enacted.
    The visible light portion beyond the dark bar indicates the difference.

    Tavory (2024): RAI alone is insufficient. This chart depicts which states have RAI 
    coverage without EoC coverage. 
    - Bottom-right quadrant of scatter but more readable.

    """
    dff = df[df["bill_count"] > 0].copy()
    dff["eoc_gap"] = dff["eoc_covered"] - dff["eoc_enacted_count"].fillna(0)
    dff = dff.sort_values("eoc_gap", ascending=True)

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            "Ethics of Care — Proposed vs. Enacted",
            "Responsible AI — Proposed vs. Enacted",
        ),
        horizontal_spacing=0.12,
    )

    # ── Left panel — EoC ──────────────────────────────────────
    fig.add_trace(
        go.Bar(
            y=dff["state"],
            x=dff["eoc_covered"],
            name="Proposed",
            orientation="h",
            marker_color="#c6dbef",
            legendgroup="proposed",
            showlegend=True,
            hovertemplate="<b>%{y}</b><br>EoC proposed: %{x} of 8<extra></extra>",
        ),
        row=1, col=1,
    )
    fig.add_trace(
        go.Bar(
            y=dff["state"],
            x=dff["eoc_enacted_count"],
            name="Enacted",
            orientation="h",
            marker_color="#084594",
            legendgroup="enacted",
            showlegend=True,
            hovertemplate="<b>%{y}</b><br>EoC enacted: %{x} of 8<extra></extra>",
        ),
        row=1, col=1,
    )

    # ── Right panel — RAI ─────────────────────────────────────
    fig.add_trace(
        go.Bar(
            y=dff["state"],
            x=dff["rai_covered"],
            name="Proposed",
            orientation="h",
            marker_color="#fdd0a2",
            legendgroup="proposed",
            showlegend=False,
            hovertemplate="<b>%{y}</b><br>RAI proposed: %{x} of 17<extra></extra>",
        ),
        row=1, col=2,
    )
    fig.add_trace(
        go.Bar(
            y=dff["state"],
            x=dff["rai_enacted_count"],
            name="Enacted",
            orientation="h",
            marker_color="#8c2d04",
            legendgroup="enacted",
            showlegend=False,
            hovertemplate="<b>%{y}</b><br>RAI enacted: %{x} of 17<extra></extra>",
        ),
        row=1, col=2,
    )

    fig.update_layout(
        barmode="overlay",
        height=750,
        margin={"r": 40, "t": 60, "l": 60, "b": 40},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Georgia, serif", "size": 11},
        legend={
            "orientation": "h",
            "y": 1.08,
            "x": 0.3,
            "font": {"size": 11},
        },
    )

    fig.update_xaxes(range=[0, 9], gridcolor="#f0ede8", title_text="Tags covered (of 8)", col=1)
    fig.update_xaxes(range=[0, 18], gridcolor="#f0ede8", title_text="Tags covered (of 17)", col=2)
    fig.update_yaxes(gridcolor="#f0ede8", tickfont={"size": 10})

    return fig


if __name__ == "__main__":
    from mhai.fetch import fetch_bills
    from mhai.index import compute_state_index

    df = fetch_bills()
    idx = compute_state_index(df)
    fig = make_choropleth(idx)
    fig.show()