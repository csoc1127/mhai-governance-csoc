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
from mhai.config import EOC_TAGS


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
    dff = dff.sort_values("eoc_enacted_count", ascending=True)

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

def make_tag_coverage(df_bills: pd.DataFrame) -> go.Figure:
    """
    Stacked horizontal bar chart - EoC tag presence across all MH-AI bills.

    For each of the 8 EoC tags, shows bill inclusion amount, split by enacted vs proposed.
    Sorted by enacted count ascending.

    No state-level analysis here, tag level-only.
    The distribution should reveal which protections legislatures consistently
    include and which they omit. 

    Data: Shumate et al. (2025) tag definitions, Table 2.
    Framework: Tavory (2024) EoC tag mapping.
    
    """
    EOC_TAG_CONTEXT = {
    "opt_out": {
        "shumate": "Provides for the ability to opt out of AI services in favor of receiving equivalent human-delivered health services.",
        "tavory": "Tavory (2024) identifies this as non-negotiable — vulnerable users must have a clear exit pathway to human care.",
    },
    "malpractice": {
        "shumate": "Pertains to liability allocation for AI-related harm, including assigning responsibility to deployers, developers, or practitioners.",
        "tavory": "Tavory's care-with principle: accountability must follow engineering decisions. Without this, developers externalize harm onto clinicians.",
    },
    "event_reporting": {
        "shumate": "Creates a system for reporting adverse events, near misses, or other safety events involving MH-AI.",
        "tavory": "Tronto's responsiveness element: care requires monitoring how it lands. No reporting system means no feedback loop.",
    },
    "human_in_the_loop": {
        "shumate": "Explicitly requires a human to monitor, approve, or participate in an essential part of the MH-AI service.",
        "tavory": "Tavory requires developers to build in human connection pathways — AI cannot replace the therapeutic relationship.",
    },
    "safety_standards": {
        "shumate": "Pertains to safety standards including human overrides, emergency protocols, or prohibitions on high-risk uses.",
        "tavory": "Tronto's attentiveness element: recognizing user needs requires active safety infrastructure, not passive compliance.",
    },
    "practitioner_responsibilities": {
        "shumate": "Applies requirements on practitioners related to their use of AI systems.",
        "tavory": "Tronto's responsibility element — but Tavory warns against displacing accountability onto clinicians who cannot audit algorithms.",
    },
    "vulnerable_populations": {
        "shumate": "Creates responsibilities related to vulnerable populations including older adults, children, disabled, and foreign-language speakers.",
        "tavory": "Fineman's universal vulnerability framework: vulnerability is contextual and ongoing, not a fixed group attribute.",
    },
    "disclosure_consent": {
        "shumate": "Implements requirements to disclose AI system use or features and obtain consent.",
        "tavory": "Informed consent obligation — NASW Code 1.03a. Without meaningful disclosure, autonomy is performative.",
    },
}
    TAG_LABELS = {
        "vulnerable_populations":        "Vulnerable Populations",
        "safety_standards":              "Safety Standards",
        "human_in_the_loop":             "Human-in-the-Loop",
        "practitioner_responsibilities": "Practitioner Responsibilities",
        "malpractice":                   "Malpractice / Liability",
        "event_reporting":               "Event Reporting",
        "opt_out":                       "Opt-Out Right",
        "disclosure_consent":            "Disclosure / Consent",
    }

    enacted = df_bills[df_bills["status"] == "Enacted"]
    proposed = df_bills[df_bills["status"] != "Enacted"]

    records = []
    for tag in EOC_TAGS:
        context = EOC_TAG_CONTEXT.get(tag, {})
        records.append({
            "tag": TAG_LABELS[tag],
            "enacted": int(enacted[tag].sum()),
            "proposed": int(proposed[tag].sum()),
            "shumate": context.get("shumate", ""),
            "tavory": context.get("tavory", ""),
        })

    tag_df = pd.DataFrame(records).sort_values("enacted", ascending=False)
    customdata = tag_df[["shumate", "tavory"]].values

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=tag_df["tag"],
        x=tag_df["proposed"],
        name="Proposed only",
        orientation="h",
        marker_color="#c6dbef",
        customdata=customdata,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Proposed bills: %{x}<br><br>"
            "<i>%{customdata[0]}</i><br><br>"
            "%{customdata[1]}"
            "<extra></extra>"
        ),
    ))

    fig.add_trace(go.Bar(
        y=tag_df["tag"],
        x=tag_df["enacted"],
        name="Enacted",
        orientation="h",
        marker_color="#084594",
        customdata=customdata,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Enacted bills: %{x}<br><br>"
            "<i>%{customdata[0]}</i><br><br>"
            "%{customdata[1]}"
            "<extra></extra>"
        ),
    ))

    fig.update_layout(
        barmode="overlay",
        height=420,
        margin={"r": 40, "t": 20, "l": 0, "b": 40},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Georgia, serif", "size": 11},
        legend={
            "orientation": "h",
            "y": 1.08,
            "x": 0,
            "font": {"size": 11},
        },
        xaxis={
            "title": "Number of bills",
            "gridcolor": "#f0ede8",
        },
        yaxis={"gridcolor": "#f0ede8"},
    )

    return fig



if __name__ == "__main__":
    from mhai.fetch import fetch_bills
    from mhai.index import compute_state_index

    df = fetch_bills()
    idx = compute_state_index(df)
    fig = make_choropleth(idx)
    fig.show()