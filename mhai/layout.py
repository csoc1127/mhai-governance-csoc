"""
layout.py

Defines the single-page scrollable Dash layout for the
MH-AI Governance Dashboard.

Design: card-based, single scroll, section-by-section.
Styled to match academic presentation standards.
"""
from dash import dcc, html
from mhai.figures import make_choropleth, make_scatter

# ── Style constants ───────────────────────────────────────────
PAGE_STYLE = {
    "maxWidth": "1200px",
    "margin": "0 auto",
    "padding": "24px 24px 56px 24px",
    "fontFamily": "Georgia, serif",
    "backgroundColor": "#f4f4f1",
}

CARD_STYLE = {
    "backgroundColor": "white",
    "border": "1px solid #e0ddd5",
    "borderRadius": "12px",
    "padding": "24px",
    "marginBottom": "22px",
    "boxShadow": "0 1px 4px rgba(0,0,0,0.06)",
}

SECTION_HEADER_STYLE = {
    "fontSize": "28px",
    "fontWeight": "700",
    "marginBottom": "10px",
    "color": "#1a1a2e",
}

SUBSECTION_HEADER_STYLE = {
    "fontSize": "18px",
    "fontWeight": "600",
    "marginTop": "0",
    "marginBottom": "8px",
    "color": "#1a1a2e",
}

BODY_TEXT_STYLE = {
    "fontSize": "15px",
    "lineHeight": "1.8",
    "color": "#444",
    "marginBottom": "0",
}

KICKER_STYLE = {
    "fontSize": "12px",
    "fontWeight": "700",
    "textTransform": "uppercase",
    "letterSpacing": "0.06em",
    "color": "#084594",
    "marginBottom": "8px",
}

LIMITATION_STYLE = {
    "fontSize": "13px",
    "lineHeight": "1.7",
    "color": "#666",
    "borderLeft": "3px solid #084594",
    "paddingLeft": "12px",
    "marginTop": "12px",
}

STAT_LABEL = {
    "fontSize": "12px",
    "color": "#999",
    "margin": "0 0 4px",
    "textTransform": "uppercase",
    "letterSpacing": "0.04em",
}

STAT_SUBTEXT = {
    "fontSize": "12px",
    "color": "#999",
    "margin": "4px 0 0",
}


def make_layout(df_state):
    return html.Div(
        style=PAGE_STYLE,
        children=[

            # ── Hero ──────────────────────────────────────────
            html.Div(
                style=CARD_STYLE,
                children=[
                    html.Div(
                        "MH-AI Governance Dashboard · MSCAPP · University of Chicago",
                        style=KICKER_STYLE,
                    ),
                    html.H1(
                        "Regulating AI in Mental Health: Efficacy, Not Performance",
                        style={
                            "fontSize": "36px",
                            "fontWeight": "700",
                            "marginTop": "0",
                            "marginBottom": "14px",
                            "color": "#1a1a2e",
                            "lineHeight": "1.3",
                        },
                    ),
                    html.P(
                        "Between 2022 and 2025, U.S. state legislatures introduced 793 bills "
                        "touching artificial intelligence and mental health. 143 were substantively "
                        "relevant. 20 were enacted. This dashboard asks not how many bills were "
                        "introduced — but whether the ones that passed actually protect anyone.",
                        style=BODY_TEXT_STYLE,
                    ),
                    html.Div(
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "1fr 1fr",
                            "gap": "20px",
                            "marginTop": "20px",
                        },
                        children=[
                            html.Div(
                                style={
                                    "backgroundColor": "#f4f4f1",
                                    "borderRadius": "10px",
                                    "padding": "16px",
                                    "borderLeft": "4px solid #084594",
                                },
                                children=[
                                    html.H4(
                                        "The Ethical Gap",
                                        style={
                                            "margin": "0 0 6px",
                                            "color": "#084594",
                                            "fontSize": "14px",
                                            "fontWeight": "700",
                                            "textTransform": "uppercase",
                                            "letterSpacing": "0.04em",
                                        },
                                    ),
                                    html.P(
                                        "Dominant AI regulation treats users as autonomous "
                                        "rational agents. Mental health AI users are not. "
                                        "They are in crisis, forming attachments, disclosing "
                                        "intimate information under distress. The Ethics of Care "
                                        "framework — grounded in social work values — measures "
                                        "the relational protections that standard regulatory "
                                        "frameworks ignore.",
                                        style={**BODY_TEXT_STYLE, "fontSize": "14px"},
                                    ),
                                ],
                            ),
                            html.Div(
                                style={
                                    "backgroundColor": "#f4f4f1",
                                    "borderRadius": "10px",
                                    "padding": "16px",
                                    "borderLeft": "4px solid #A32D2D",
                                },
                                children=[
                                    html.H4(
                                        "The Legislative Gap",
                                        style={
                                            "margin": "0 0 6px",
                                            "color": "#A32D2D",
                                            "fontSize": "14px",
                                            "fontWeight": "700",
                                            "textTransform": "uppercase",
                                            "letterSpacing": "0.04em",
                                        },
                                    ),
                                    html.P(
                                        "States introduce bills for political positioning, "
                                        "not patient protection. Massachusetts has perfect "
                                        "proposed EoC coverage — and zero enacted bills. "
                                        "This dashboard measures the gap between legislative "
                                        "performance and actual governance using binary coverage "
                                        "scoring across care-aligned and responsible AI tag "
                                        "dimensions.",
                                        style={**BODY_TEXT_STYLE, "fontSize": "14px"},
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        "Data: Shumate et al. (2025) JMIR Mental Health · "
                        "Framework: Tavory (2024) JMIR Mental Health · "
                        "Built by Ciara Staveley-O'Carroll, MSCAPP, University of Chicago",
                        style={
                            "fontSize": "12px",
                            "color": "#999",
                            "marginTop": "16px",
                            "borderTop": "1px solid #e0ddd5",
                            "paddingTop": "12px",
                        },
                    ),
                ],
            ),

            # ── Stats ─────────────────────────────────────────
            html.Div(
                style={
                    **CARD_STYLE,
                    "display": "grid",
                    "gridTemplateColumns": "repeat(5, 1fr)",
                    "gap": "16px",
                    "padding": "20px 24px",
                },
                children=[
                    html.Div(
                        style={"borderRight": "1px solid #e0ddd5", "paddingRight": "16px"},
                        children=[
                            html.P("Bills reviewed", style=STAT_LABEL),
                            html.P("793", style={"fontSize": "32px", "fontWeight": "700", "color": "#1a1a2e", "margin": "0"}),
                            html.P("143 relevant · 20 enacted", style=STAT_SUBTEXT),
                        ],
                    ),
                    html.Div(
                        style={"borderRight": "1px solid #e0ddd5", "paddingRight": "16px"},
                        children=[
                            html.P("States silent", style=STAT_LABEL),
                            html.P("12 of 50", style={"fontSize": "32px", "fontWeight": "700", "color": "#A32D2D", "margin": "0"}),
                            html.P("Zero relevant bills introduced", style=STAT_SUBTEXT),
                        ],
                    ),
                    html.Div(
                        style={"borderRight": "1px solid #e0ddd5", "paddingRight": "16px"},
                        children=[
                            html.P("Median EoC enacted", style=STAT_LABEL),
                            html.P("0%", style={"fontSize": "32px", "fontWeight": "700", "color": "#A32D2D", "margin": "0"}),
                            html.P("Majority enacted nothing care-based", style=STAT_SUBTEXT),
                        ],
                    ),
                    html.Div(
                        style={"borderRight": "1px solid #e0ddd5", "paddingRight": "16px"},
                        children=[
                            html.P("Mean EoC enacted", style=STAT_LABEL),
                            html.P("10%", style={"fontSize": "32px", "fontWeight": "700", "color": "#084594", "margin": "0"}),
                            html.P("Pulled up by CO and UT outliers", style=STAT_SUBTEXT),
                        ],
                    ),
                    html.Div(
                        children=[
                            html.P("Explicitly MH-AI", style=STAT_LABEL),
                            html.P("28 of 143", style={"fontSize": "32px", "fontWeight": "700", "color": "#854F0B", "margin": "0"}),
                            html.P("Rest incidental to broader AI law", style=STAT_SUBTEXT),
                        ],
                    ),
                ],
            ),

            # ── Map ───────────────────────────────────────────
            html.Div(
                style=CARD_STYLE,
                children=[
                    html.Div("Interactive section 1 of 3", style=KICKER_STYLE),
                    html.H2(
                        "Ethics of Care Enacted Index by State",
                        style=SECTION_HEADER_STYLE,
                    ),
                    html.P(
                        "Each state is colored by its Ethics of Care Enacted Index — "
                        "the percentage of 8 care-based legislative protections covered "
                        "by at least one enacted bill. Proposed bills are excluded. "
                        "A state that introduced comprehensive legislation but passed "
                        "none scores the same as a state that introduced nothing.",
                        style=BODY_TEXT_STYLE,
                    ),
                    html.Div(
                        "Hover over a state to see its score, bill count, "
                        "and which protections are missing.",
                        style={**BODY_TEXT_STYLE, "marginTop": "8px", "color": "#666", "fontSize": "13px"},
                    ),
                    html.Div(
                        style={"marginTop": "16px"},
                        children=[
                            dcc.Graph(
                                id="choropleth",
                                figure=make_choropleth(df_state),
                                style={"height": "500px"},
                                config={"displaylogo": False},
                            )
                        ],
                    ),
                    html.Div(
                        "Limitation: tag presence does not confirm scope, "
                        "enforceability, or population coverage. Per Shumate et al. "
                        "(2025): tag assignment was descriptive rather than qualitative.",
                        style=LIMITATION_STYLE,
                    ),
                ],
            ),

            # ── Scatter ───────────────────────────────────────
            html.Div(
                style=CARD_STYLE,
                children=[
                    html.Div("Interactive section 2 of 3", style=KICKER_STYLE),
                    html.H2(
                        "Performative vs. Protective: The Legislative Gap",
                        style=SECTION_HEADER_STYLE,
                    ),
                    html.P(
                        "Each dot is an active state. X axis shows Responsible AI "
                        "protections actually enacted. Y axis shows Ethics of Care "
                        "protections actually enacted. Dot size reflects total bills "
                        "introduced. Color reflects enactment rate. "
                        "States in the bottom-left introduced legislation but passed nothing. "
                        "States in the bottom-right regulate AI technically "
                        "but ignore relational protections entirely.",
                        style=BODY_TEXT_STYLE,
                    ),
                    html.Div(
                        style={"marginTop": "16px"},
                        children=[
                            dcc.Graph(
                                id="scatter",
                                figure=make_scatter(df_state),
                                style={"height": "500px"},
                                config={"displaylogo": False},
                            )
                        ],
                    ),
                    html.Div(
                        "Proposed bills excluded. Both indices reflect enacted "
                        "legislation only. Dot size is total bills introduced — "
                        "large dots near the origin represent performative legislative "
                        "activity without enacted protection.",
                        style=LIMITATION_STYLE,
                    ),
                ],
            ),

        ],
    )