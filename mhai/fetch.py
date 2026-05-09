"""
fetch.py

Fetches MH-AI legislative bill data from Shumate et al. (2025) public
database API. Plan B to local CSV if API is unavailable.

Source: https://governing-ai-in-mental-health.digitalpsychpapers.org
Paper: Shumate et al. (2025) JMIR Mental Health, 12, e80739

Inputs: Live API or data/mh_ai_bills_raw.csv

Outputs: pd.DataFrame, one row per bill, bool cols for all 25 tags

"""
import requests
import pandas as pd
from pathlib import Path
from mhai.config import API_URL, FALLBACK_CSV

def fetch_bills() -> pd.DataFrame:
    """
    Ideally fetch all MH-AI bills from live API,
    otherwise resort to local CSV if unavailable
    
    Returns: pd.DataFrame, one row per bill, boolean tag columns
    """
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        df = pd.DataFrame(response.json())
        df.to_csv(FALLBACK_CSV, index=False) #Fallback stays fresh if API is available
        print(f"success! fetched {len(df)} bills from live API)")
        return df
    except requests.RequestException as e:
        print(f"API unavailable({e}, resorting to csv)")
        return pd.read_csv(FALLBACK_CSV)
    
if __name__ == "__main__":
    df = fetch_bills()
    print(df.head())
    print(f"\nColumns: {list(df.columns)}")
    print(f"Shape: {df.shape}")