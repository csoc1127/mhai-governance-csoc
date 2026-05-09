"""
index.py

Computes per-state Ethics of Care (EoC) and Responsible AI (RAI) 
indices derived from MH-AI bill data.

Methodology: Binary coverage scoring - foreach tag, a state either has
it covered by at least one bill (1) or not (0), regarless of
how many bills address it. This approach captures regulatory breadth
over legislative volume, and avoids overcounting states
with multiple bills on the same tag (looking at you CA).

EoC Index: (EoC tags covered / 8) * 10, range 0-10
RAI Index: (RAI tags covered / 17) * 10, range 0-10

Enacted-only variance computed separately for sensitivity analysis.

Theoretical basis: EoC tags operationalize Tavory(2024) ethics of care framework
and Tront's five elements of care; RAI tags reflect "responsible AI" principles Tavory 
argues are necessary but insufficient for mental health contexts specifically.

    Tag definitions: Shumate et al. (2025) Table 2, JMIR Mental Health
    Index methodology: binary coverage per ArcGIS Pro composite
    index standards (Esri, 2024); equal weighting acknowledged
    as a limitation — see paper limitations section.
    See config.py for tag definitions.

Limitations: Presence-based only. A tag that is marked present does not
confirm scope, enforcability, or population coverage quality.
Per Shumate et al. (2025): "Tag assignment was descriptive rather than qualitative,
signaling only that the tag's specific topic was addressed in the bill in
some form." Future work could explore more nuanced coding of tag coverage quality.

Input: pd.DataFrame from fetch.fetch_bills()

Output: pd.DataFrame with one row per state
Columns: state (abbreviation), state_name, eoc_index, rai_index, 
eoc_covered (raw count of how many of the 8 EOC tags covered), rai_covered, bill_count (total bills),
enacted_count, explicit_count(explicitly mentions MH-AI), eoc_enacted_index, rai_enacted_index

"""
import pandas as pd
from mhai.config import EOC_TAGS, RESPONSIBLE_AI_TAGS, STATE_NAMES

def compute_state_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes EoC and RAI indices per state based on binary coverage of tags for 
    all 50 states.
    
    For each state, checks if at least one bill covers each tag.
    Scores reflect breadth of protection (how many distinct
    care-based or responsible AI provisions exist), not legislative volume.  

    Args:
        df: pd.DataFrame from fetch.fetch_bills()

    Returns: DataFrame with one row per state, both index scores, 
    and supporting columns for viz and analysis.

    """
    records =[]

    for state, group in df.groupby("state"):
        #Binary coverage: if any bill in the state covers the tag, it's a 1 for that tag
        # using any(), 8 vectorized operations > 143 row iterations
        eoc_covered = [tag for tag in EOC_TAGS if group[tag].any()]
        rai_covered = [tag for tag in RESPONSIBLE_AI_TAGS if group[tag].any()]

        #Enacted bills - sensitivity check
        enacted = group[group["status"] == "Enacted"]
        eoc_enacted = [tag for tag in EOC_TAGS if not enacted.empty and enacted[tag].any()]
        rai_enacted = [tag for tag in RESPONSIBLE_AI_TAGS if not enacted.empty and enacted[tag].any()]

        records.append({
            "state": state,
            "bill_count": len(group),
            "enacted_count": len(enacted),
            "enacted_pct": round(len(enacted) / len(group) * 100, 1) if len(group) > 0 else 0,
            "explicit_count": (group["taxonomy_code"] == "E").sum(),
            "eoc_covered": len(eoc_covered),
            "rai_covered": len(rai_covered),
            "eoc_enacted_count": len(eoc_enacted),
            "rai_enacted_count": len(rai_enacted),
            "eoc_index": round((len(eoc_covered) / len(EOC_TAGS)) * 10, 2),
            "rai_index": round((len(rai_covered) / len(RESPONSIBLE_AI_TAGS)) * 10, 2),
            "eoc_enacted_index": round((len(eoc_enacted) / len(EOC_TAGS)) * 10, 2),
            "rai_enacted_index": round((len(rai_enacted) / len(RESPONSIBLE_AI_TAGS)) * 10, 2),
            "eoc_tags_covered": ", ".join(eoc_covered),
            "eoc_tags_missing": ", ".join([t for t in EOC_TAGS if t not in eoc_covered]),
        })
    
    # Build state dataframe - zero rows for silent states
    all_states = pd.DataFrame({
        "state": list(STATE_NAMES.keys()),
        "state_name":list(STATE_NAMES.values())
    })

    result = all_states.merge(pd.DataFrame(records), on="state", how="left").fillna(0)
    result["eoc_index"] = result["eoc_index"].round(2)
    result["rai_index"] = result["rai_index"].round(2)
    result["eoc_tags_missing"] = result["eoc_tags_missing"].replace(0, "none covered")
    result["eoc_tags_covered"] = result["eoc_tags_covered"].replace(0, "")

    return result

# if __name__ == "__main__":
#     from mhai.fetch import fetch_bills
#     df = fetch_bills()
#     idx = compute_state_index(df)
#     print(idx[["state", "bill_count", "enacted_pct", "eoc_index", "eoc_enacted_index", "rai_index"]]
#       .sort_values("eoc_index", ascending=False)
#       .head(15)
#       .to_string(index=False))
#     print(f"\nSilent states: {(idx['bill_count'] == 0).sum()}")
#     print(f"Mean EoC (active states): {idx[idx['bill_count'] > 0]['eoc_index'].mean():.2f}")
#     print(f"Mean RAI (active states): {idx[idx['bill_count'] > 0]['rai_index'].mean():.2f}")
if __name__ == "__main__":
    from mhai.fetch import fetch_bills

    df = fetch_bills()
    idx = compute_state_index(df)

    print(f"Total states: {len(idx)}")
    print(f"Silent states: {(idx['bill_count'] == 0).sum()}")
    print(f"Mean EoC (active): {idx[idx['bill_count'] > 0]['eoc_index'].mean():.2f}")
    print(f"Mean RAI (active): {idx[idx['bill_count'] > 0]['rai_index'].mean():.2f}")
    print(f"\nTop 5 by EoC enacted:")
    print(idx[["state", "eoc_enacted_index", "enacted_pct"]]
          .sort_values("eoc_enacted_index", ascending=False)
          .head(5)
          .to_string(index=False))