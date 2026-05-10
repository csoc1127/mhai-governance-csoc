# MH-AI Governance Dashboard
## Regulating AI in Mental Health: Efficacy, Not Performance

This dashboard is the analytical component of a graduate research paper completed at the University of Chicago Crown Family School of Social Work, Spring 2026. The paper argues that the United States prioritizes the perception of legislative productivity over the efficacy of Artificial Intelligence regulation that specifically pertains to mental health, and that the Ethics of Care framework — already foundational to social work practice — provides the most clinically coherent path to reform.

The dashboard tries to empirically implement this argument. It applies an original **Ethics of Care Alignment Index** to the 50-state legislative dataset from Shumate et al. (2025), scoring each state on whether its enacted laws cover the eight care-based protections Tavory (2024) identifies as essential for any AI system operating in a therapeutic space.

Key findings: states that introduce the most bills are not the states that enact the most protections. Legislative volume is not legislative protection. The median enacted EoC index across active states is zero — most states have passed nothing that Tavory identifies as a required developer protection. Across all 50 states and three years of legislative activity, only 2 enacted bills anywhere in the country guarantee a user the right to a human alternative, and only 1 enacted bill holds a developer accountable for harm. States with the highest proposed coverage — Massachusetts, Rhode Island, Illinois, Texas — enacted zero of those protections into law.

---

## Three Visuals

- **Ethics of Care Enacted Index by State** — choropleth map showing enacted EoC coverage per state. Proposed bills are excluded. A state that introduced comprehensive legislation but passed none scores the same as a state that introduced nothing.
- **Performative vs. Protective: The Legislative Gap** — side-by-side bar chart comparing proposed vs. enacted coverage across EoC and Responsible AI tags by state, sorted by EoC gap descending.
- **Which Ethics of Care Protections Are Legislatures Enacting?** — tag-level chart showing which of the eight care-based protections most rarely survive into enacted law, with Shumate definitions and Tavory connections embedded in hover tooltips.

---

## The Eight EoC Tags

Each tag is drawn from Shumate et al.'s (2025) 25-tag coding system. Selection is justified by explicit correspondence to Tronto's five elements of care and Tavory's proposed developer obligations.

| Tag | Tavory Connection |
|-----|------------------|
| Vulnerable populations | Fineman universal vulnerability framework |
| Safety standards | Tronto attentiveness — recognizing user needs |
| Human-in-the-loop | Right to human connection option |
| Practitioner responsibilities | Tronto responsibility element |
| Malpractice / liability | Accountability must follow engineering decisions |
| Event reporting | Tronto responsiveness — monitoring how care lands |
| Opt-out right | Non-negotiable right to human alternative |
| Disclosure / consent | Informed consent obligation — NASW Code 1.03a |

---

## Screenshots

### Ethics of Care Index by State
![Choropleth](docs/assets/choropleth.png)

### Legislative Gap
![Gap Bar](docs/assets/gap_bar.png)

### Tag Coverage
![Tag Coverage](docs/assets/tag_coverage.png)

---

## Citations

### Primary Sources

Shumate, J. N., Rozenblit, E., Flathers, M., Larrauri, C. A., Hau, C., Xia, W., Torous, E. N., & Torous, J. (2025). Governing AI in mental health: 50-state legislative review. *JMIR Mental Health*, 12, e80739. https://doi.org/10.2196/80739

Tavory, T. (2024). Regulating AI in mental health: Ethics of care perspective. *JMIR Mental Health*, 11, e58493. https://doi.org/10.2196/58493

### Supporting Sources

Bires, J. (2026, April 30). *The future of psychosocial oncology: AI, innovation and the next era of supportive care* [Webinar]. Association of Cancer Care Centers & Association of Oncology Social Work.

Frase, H., & Daniels, O. (2023, August 11). Understanding AI harms: An overview. Center for Security and Emerging Technology, Georgetown University. https://cset.georgetown.edu/article/understanding-ai-harms-an-overview/

Gardner, C., & Frazier, K. T. (2026, April 13). The FDA needs to adjust to the reality of AI software. *Cato at Liberty*. https://www.cato.org/blog/fda-needs-adjust-reality-ai-software

Madison, J. (1788). Federalist No. 51. In *The Federalist Papers*. https://avalon.law.yale.edu/18th_century/fed51.asp

National Association of Social Workers. (2017). *NASW code of ethics*. NASW Press.

### Data

Live API: https://governing-ai-in-mental-health.digitalpsychpapers.org/api/bills

---

## How to Run

1. [Install UV](https://docs.astral.sh/uv/getting-started/installation/)
2. Clone the repo: git@github.com:csoc1127/mhai-governance-csoc.git
3. Install dependencies:
4. Run the dashboard:
5. The terminal will show: "Dash is running on http://127.0.0.1:8050". Open that URL in your browser.
6. To exit, run `Ctrl + C` in the terminal.

---

## Built By

Ciara Staveley-O'Carroll — MSCAPP, University of Chicago Spring 2026

*Paper title: The Duty That Wasn't Designed: Mental Health Artificial Intelligence, Structural Harm, and the Social Work Case for an Ethics of Care Framework*