"""
layout.py

Defines the single-page scrollable Dash layout for the
MH-AI Governance Dashboard.

Design: card-based, single scroll, section-by-section.
"""
from dash import dcc, html
from mhai.figures import make_choropleth, make_eoc_gap_bar, make_rai_gap_bar, make_tag_coverage

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

NAV_STYLE = {
    "fontSize": "13px",
    "color": "#666",
    "lineHeight": "1.8",
    "borderLeft": "3px solid #e0ddd5",
    "paddingLeft": "12px",
    "marginBottom": "0",
}


def make_layout(df_state, df_bills):
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
                                        "The Care Gap",
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
                                        "Standard AI regulation assumes users are rational and "
                                        "self-protective. Mental health AI users often are not — "
                                        "they are in crisis, forming attachments, disclosing "
                                        "intimate information under distress. The ethics of care "
                                        "framework measures the relational protections that "
                                        "standard regulatory models are not designed to require.",
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
                                        "States introduce bills to signal concern — not always "
                                        "to pass law. Massachusetts introduced legislation "
                                        "covering all eight care-based protections this dashboard "
                                        "measures. None became law. This dashboard separates "
                                        "what was proposed from what actually governs.",
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
                            html.P("143 relevant · 20 became law", style=STAT_SUBTEXT),
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
                            html.P("Median care-based law", style=STAT_LABEL),
                            html.P("0 of 8", style={"fontSize": "32px", "fontWeight": "700", "color": "#A32D2D", "margin": "0"}),
                            html.P("Most states passed nothing care-based", style=STAT_SUBTEXT),
                        ],
                    ),
                    html.Div(
                        style={"borderRight": "1px solid #e0ddd5", "paddingRight": "16px"},
                        children=[
                            html.P("Mean care-based law", style=STAT_LABEL),
                            html.P("10%", style={"fontSize": "32px", "fontWeight": "700", "color": "#084594", "margin": "0"}),
                            html.P("Pulled up by CO and UT", style=STAT_SUBTEXT),
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

            # ── Dashboard guide ───────────────────────────────
            html.Div(
                style={**CARD_STYLE, "backgroundColor": "#f9f8f5"},
                children=[
                    html.Div("How to read this dashboard", style=KICKER_STYLE),
                    html.P(
                        "Section 1 shows which states have enacted care-based protections into law — "
                        "the geographic picture of who governs and who does not. "
                        "Section 2 shows the gap between what states introduced and what actually passed, "
                        "separately for care-based protections and standard regulatory protections. "
                        "Section 3 shows which specific protections are most absent from enacted law nationally — "
                        "and whether even bills written explicitly for mental health AI closed those gaps.",
                        style=NAV_STYLE,
                    ),
                ],
            ),

            # ── Map ───────────────────────────────────────────
            html.Div(
                style=CARD_STYLE,
                children=[
                    html.Div("Interactive section 1 of 3", style=KICKER_STYLE),
                    html.H2(
                        "Care-Based Protections Enacted by State",
                        style=SECTION_HEADER_STYLE,
                    ),
                    html.P(
                        "Each state is colored by how many of the eight care-based protections "
                        "identified in this analysis are covered by at least one enacted bill. "
                        "Proposed legislation is excluded. A state that introduced comprehensive "
                        "bills but passed none is indistinguishable from a state that introduced nothing — "
                        "because for the person using a mental health AI tool in that state, "
                        "the outcome is the same.",
                        style=BODY_TEXT_STYLE,
                    ),
                    html.Div(
                        "Hover over any state to see its enacted coverage, bill count, "
                        "and which protections have not yet become law.",
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
                        "Tag presence does not confirm scope, enforceability, or population coverage. "
                        "Per Shumate et al. (2025): tag assignment was descriptive rather than qualitative. "
                        "A bill tagged 'vulnerable populations' focused only on minors receives the same "
                        "score as one covering cognitive disability and limited English proficiency.",
                        style=LIMITATION_STYLE,
                    ),
                ],
            ),

            # ── EoC Gap Bar ───────────────────────────────────
            html.Div(
                style=CARD_STYLE,
                children=[
                    html.Div("Interactive section 2a of 3", style=KICKER_STYLE),
                    html.H2(
                        "Care-Based Protections: What Was Introduced vs. What Became Law",
                        style=SECTION_HEADER_STYLE,
                    ),
                    html.P(
                        "The eight protections measured here are the ones most directly tied to "
                        "vulnerable users in therapeutic relationships: crisis response, the right "
                        "to speak to a human, informed consent, continuity of care, and developer "
                        "accountability for harm. Light bars show what was introduced. "
                        "Dark bars show what became law. "
                        "States at the top passed the most. States at the bottom — including some "
                        "of the most legislatively active — passed nothing. "
                        "Hover the dark bar to see exactly which protections your state has "
                        "and has not enacted.",
                        style=BODY_TEXT_STYLE,
                    ),
                    html.Div(
                        style={"marginTop": "16px"},
                        children=[
                            dcc.Graph(
                                id="eoc-gap-bar",
                                figure=make_eoc_gap_bar(df_state),
                                style={"height": "750px"},
                                config={"displaylogo": False},
                            )
                        ],
                    ),
                    html.Div(
                        "Sorted by enacted coverage — most at top. "
                        "CO and UT at top: passed everything they introduced. "
                        "MA, RI, IL, TX near bottom: introduced protections covering all 8 categories, "
                        "passed none. "
                        "States that proposed nothing and passed nothing appear at the very bottom.",
                        style=LIMITATION_STYLE,
                    ),
                ],
            ),

            # ── RAI Gap Bar ───────────────────────────────────
            html.Div(
                style=CARD_STYLE,
                children=[
                    html.Div("Interactive section 2b of 3", style=KICKER_STYLE),
                    html.H2(
                        "Standard Regulatory Protections: What Was Introduced vs. What Became Law",
                        style=SECTION_HEADER_STYLE,
                    ),
                    html.P(
                        "These 17 protections — transparency, data privacy, bias auditing, "
                        "civil penalties, consumer protection — represent the dominant model "
                        "of AI regulation. They are technically important. "
                        "They were designed for rational, autonomous users. "
                        "Compare this chart to the one above: states that appear active here "
                        "may show almost nothing on the care-based chart. "
                        "That is the gap Tavory (2024) identifies — technically regulated, "
                        "relationally unprotected.",
                        style=BODY_TEXT_STYLE,
                    ),
                    html.Div(
                        style={"marginTop": "16px"},
                        children=[
                            dcc.Graph(
                                id="rai-gap-bar",
                                figure=make_rai_gap_bar(df_state),
                                style={"height": "750px"},
                                config={"displaylogo": False},
                            )
                        ],
                    ),
                    html.Div(
                        "Sorted independently by standard regulatory enacted coverage. "
                        "State order differs from the care-based chart above — "
                        "a state prominent here may be absent above. "
                        "Texas introduced 16 of 17 standard regulatory protections. None became law.",
                        style=LIMITATION_STYLE,
                    ),
                ],
            ),

            # ── Tag Coverage ──────────────────────────────────
            html.Div(
                style=CARD_STYLE,
                children=[
                    html.Div("Interactive section 3 of 3", style=KICKER_STYLE),
                    html.H2(
                        "Which Care-Based Protections Are Legislatures Actually Passing?",
                        style=SECTION_HEADER_STYLE,
                    ),
                    html.P(
                        "Each bar shows how many bills included a specific care-based protection "
                        "— split by all bills introduced (light), all that became law (dark), "
                        "and bills written explicitly for mental health AI that became law (darkest, patterned). "
                        "The third layer answers a pointed question: even among the 28 bills that "
                        "legislators specifically wrote for mental health AI, which protections "
                        "still did not survive into law? "
                        "Protections at the top of the chart are the rarest in enacted legislation. "
                        "Hover any bar for the Shumate definition and Tavory's explanation of "
                        "why that protection matters.",
                        style=BODY_TEXT_STYLE,
                    ),
                    html.Div(
                        style={"marginTop": "16px"},
                        children=[
                            dcc.Graph(
                                id="tag-coverage",
                                figure=make_tag_coverage(df_bills),
                                style={"height": "460px"},
                                config={"displaylogo": False},
                            )
                        ],
                    ),
                    html.Div(
                        "Tag presence is binary per bill — a bill either addresses a protection "
                        "or it does not. Per Shumate et al. (2025): tag assignment was descriptive "
                        "rather than qualitative. The explicitly MH-AI layer uses taxonomy code E "
                        "from Shumate et al.'s classification system, representing bills that "
                        "directly and intentionally targeted mental health AI rather than "
                        "incidentally covering it through broader legislation.",
                        style=LIMITATION_STYLE,
                    ),
                ],
            ),
        ],
    )