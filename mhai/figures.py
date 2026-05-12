"""
figures.py

Builds Plotly figures for the MH-AI Governance Dashboard.

Functions:
- make_choropleth: US State choropleth map - EoC enacted index
- make_scatter: performative vs protective scatterplot
- make_eoc_gap_bar: proposed vs enacted care-based coverage by state (independent sort)
- make_rai_gap_bar: proposed vs enacted standard regulatory coverage by state (independent sort)
- make_tag_coverage: EoC tag presence across all bills + explicitly MH-AI bills
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from mhai.config import EOC_TAGS


def make_choropleth(df: pd.DataFrame) -> go.Figure:
    """""
    US State choropleth colored by EOC enacted index.

    Design call: uses eoc_enacted_index instead of eoc_index.
    Enacted bills represent ACTUAL governance, IE protections delivered.
    Proposed bills represent legislative intent, IE protection promised.
    This map depicts productive, qualitative legislation that became law,
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
            "eoc_enacted_index": "Care Index (enacted)",
            "eoc_index": "Care Index (proposed)",
            "bill_count": "Total bills",
            "enacted_count": "Bills that became law",
            "enacted_pct": "% that became law",
            "eoc_tags_missing": "Protections not yet law",
        },
    )

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_colorbar={
            "title": "Care<br>Index<br>(enacted)",
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
    dff = df[df["bill_count"] > 0].copy()

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


def make_eoc_gap_bar(df: pd.DataFrame) -> go.Figure:
    """
    Horizontal bar chart — care-based protections proposed vs enacted by state.

    Design call: overlay mode where light bar is proposed, dark bar is enacted.
    The visible light portion beyond the dark bar is the performative gap.

    Sorted independently by eoc_enacted_count descending, with eoc_covered
    as tiebreaker. States that proposed everything and passed nothing surface
    near the bottom. States that passed what they proposed surface at the top.

    Tavory (2024): the care gap is not legislative inactivity — it is the
    structural absence of relational protections in what actually became law.
    This chart makes that absence state-by-state visible.

    Hover shows: what passed, what percentage of proposals became law,
    and which protections are still missing — framed as citizen rights.
    """
    dff = df[df["bill_count"] > 0].copy()

    dff["eoc_enact_pct"] = (
        dff["eoc_enacted_count"] / dff["eoc_covered"].replace(0, float("nan")) * 100
    ).fillna(0).round(0).astype(int)

    dff = dff.sort_values(
        ["eoc_enacted_count", "eoc_covered"],
        ascending=[True, True]
    )

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=dff["state"],
        x=dff["eoc_covered"],
        name="Introduced",
        orientation="h",
        marker_color="#c6dbef",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Introduced: %{x} of 8 care-based protections<br>"
            "<i>Hover the dark bar to see what became law</i>"
            "<extra></extra>"
        ),
    ))

    fig.add_trace(go.Bar(
        y=dff["state"],
        x=dff["eoc_enacted_count"],
        name="Became law",
        orientation="h",
        marker_color="#084594",
        customdata=dff[["eoc_enact_pct", "eoc_tags_missing"]].values,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "%{x} of 8 care-based protections became law<br>"
            "%{customdata[0]}% of what was introduced passed<br><br>"
            "<i>Not yet law in your state: %{customdata[1]}</i>"
            "<extra></extra>"
        ),
    ))

    fig.update_layout(
        barmode="overlay",
        height=750,
        margin={"r": 40, "t": 40, "l": 60, "b": 40},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Georgia, serif", "size": 11},
        legend={
            "orientation": "h",
            "y": 1.04,
            "x": 0,
            "font": {"size": 11},
        },
        xaxis={
            "range": [0, 9],
            "gridcolor": "#f0ede8",
            "title": "Care-based protections (of 8)",
        },
        yaxis={"gridcolor": "#f0ede8", "tickfont": {"size": 10}},
        title={
            "text": "Care-Based Protections — Introduced vs. Became Law",
            "font": {"size": 14, "family": "Georgia, serif"},
            "x": 0.5,
            "xanchor": "center",
        },
    )

    return fig


def make_rai_gap_bar(df: pd.DataFrame) -> go.Figure:
    """
    Horizontal bar chart — standard regulatory protections proposed vs enacted by state.

    Design call: overlay mode, independently sorted from EoC chart.
    Each panel tells its own story — state order is not shared.

    Sorted by rai_enacted_count descending with rai_covered as tiebreaker.

    Tavory (2024): RAI alone is insufficient. This chart is the comparison
    panel — states high on RAI but low on EoC (visible by comparing to the
    care-based chart) are technically regulated but relationally unprotected.
    That is Tavory's argument made visible as two separate ranked lists.
    """
    dff = df[df["bill_count"] > 0].copy()

    dff["rai_enact_pct"] = (
        dff["rai_enacted_count"] / dff["rai_covered"].replace(0, float("nan")) * 100
    ).fillna(0).round(0).astype(int)

    dff = dff.sort_values(
        ["rai_enacted_count", "rai_covered"],
        ascending=[True, True]
    )

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=dff["state"],
        x=dff["rai_covered"],
        name="Introduced",
        orientation="h",
        marker_color="#fdd0a2",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Introduced: %{x} of 17 standard regulatory protections<br>"
            "<i>Hover the dark bar to see what became law</i>"
            "<extra></extra>"
        ),
    ))

    fig.add_trace(go.Bar(
        y=dff["state"],
        x=dff["rai_enacted_count"],
        name="Became law",
        orientation="h",
        marker_color="#8c2d04",
        customdata=dff[["rai_enact_pct"]].values,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "%{x} of 17 standard regulatory protections became law<br>"
            "%{customdata[0]}% of what was introduced passed"
            "<extra></extra>"
        ),
    ))

    fig.update_layout(
        barmode="overlay",
        height=750,
        margin={"r": 40, "t": 40, "l": 60, "b": 40},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Georgia, serif", "size": 11},
        legend={
            "orientation": "h",
            "y": 1.04,
            "x": 0,
            "font": {"size": 11},
        },
        xaxis={
            "range": [0, 18],
            "gridcolor": "#f0ede8",
            "title": "Standard regulatory protections (of 17)",
        },
        yaxis={"gridcolor": "#f0ede8", "tickfont": {"size": 10}},
        title={
            "text": "Standard Regulatory Protections — Introduced vs. Became Law",
            "font": {"size": 14, "family": "Georgia, serif"},
            "x": 0.5,
            "xanchor": "center",
        },
    )

    return fig


def make_tag_coverage(df_bills: pd.DataFrame) -> go.Figure:
    """
    Overlay horizontal bar chart — EoC tag presence across all MH-AI bills.

    Three layers:
    1. All proposed bills (light blue)
    2. All enacted bills (dark blue)
    3. Enacted bills from explicitly MH-AI legislation only (darkest, patterned)

    Sorted by enacted count descending — most absent protections at top.

    The third layer answers a pointed question: even among the 28 bills that
    legislators specifically wrote for mental health AI, which protections
    still failed to survive into law? If opt-out and malpractice are absent
    even in explicitly MH-AI legislation, the gap is not accidental.

    No state-level analysis. Tag-level only.
    The distribution reveals which protections legislatures consistently
    include and which they consistently omit.

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
    explicit = df_bills[df_bills["taxonomy_code"] == "E"]
    explicit_enacted = explicit[explicit["status"] == "Enacted"]

    records = []
    for tag in EOC_TAGS:
        context = EOC_TAG_CONTEXT.get(tag, {})
        records.append({
            "tag": TAG_LABELS[tag],
            "enacted": int(enacted[tag].sum()),
            "proposed": int(proposed[tag].sum()),
            "explicit_enacted": int(explicit_enacted[tag].sum()),
            "shumate": context.get("shumate", ""),
            "tavory": context.get("tavory", ""),
        })

    tag_df = pd.DataFrame(records).sort_values("enacted", ascending=False)
    customdata = tag_df[["shumate", "tavory"]].values

    fig = go.Figure()

    # Layer 1 — all proposed
    fig.add_trace(go.Bar(
        y=tag_df["tag"],
        x=tag_df["proposed"],
        name="Introduced (all bills)",
        orientation="h",
        marker_color="#c6dbef",
        customdata=customdata,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Introduced in %{x} bills<br><br>"
            "<i>%{customdata[0]}</i><br><br>"
            "%{customdata[1]}"
            "<extra></extra>"
        ),
    ))

    # Layer 2 — all enacted
    fig.add_trace(go.Bar(
        y=tag_df["tag"],
        x=tag_df["enacted"],
        name="Became law (all bills)",
        orientation="h",
        marker_color="#084594",
        customdata=customdata,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Became law in %{x} bills<br><br>"
            "<i>%{customdata[0]}</i><br><br>"
            "%{customdata[1]}"
            "<extra></extra>"
        ),
    ))

    # Layer 3 — explicitly MH-AI enacted only
    fig.add_trace(go.Bar(
        y=tag_df["tag"],
        x=tag_df["explicit_enacted"],
        name="Became law (explicitly MH-AI bills only)",
        orientation="h",
        marker_color="#1a1a2e",
        marker_pattern_shape="/",
        marker_pattern_fgcolor="white",
        customdata=customdata,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Became law in %{x} bills explicitly targeting MH-AI<br><br>"
            "<i>%{customdata[0]}</i><br><br>"
            "%{customdata[1]}"
            "<extra></extra>"
        ),
    ))

    fig.update_layout(
        barmode="overlay",
        height=460,
        margin={"r": 40, "t": 20, "l": 0, "b": 40},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Georgia, serif", "size": 11},
        legend={
            "orientation": "h",
            "y": 1.10,
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