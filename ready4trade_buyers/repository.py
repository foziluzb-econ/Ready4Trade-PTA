"""Buyer-lead CSV loading and literal search."""
from __future__ import annotations
import re
from pathlib import Path
import pandas as pd

class BuyerRepository:
    def __init__(self, path: str | Path) -> None:
        self.path=Path(path); self.modified=None; self.dataframe=None
    def load(self) -> pd.DataFrame:
        try:
            modified=self.path.stat().st_mtime
            if self.dataframe is None or modified != self.modified:
                self.dataframe=pd.read_csv(self.path, dtype=str, keep_default_na=False, encoding="utf-8-sig", low_memory=False); self.modified=modified
            return self.dataframe
        except Exception:
            return pd.DataFrame()
    @staticmethod
    def search(df: pd.DataFrame, choice: str, query: str) -> pd.DataFrame:
        columns={"product":["Product Name"],"country":["Buyer From"],"hscode":["ENTUM_HS6","ENTUM_HS6_Top1"],"details":["Title","Specifications","Product Description"]}
        selected=list(df.columns) if choice=="all" else columns.get(choice, [])
        mask=pd.Series(False,index=df.index,dtype=bool)
        if choice == "hscode":
            query_text = re.sub(r"\.0+$", "", str(query).strip())
            query_digits = re.sub(r"\D", "", query_text)
            if not query_digits or len(query_digits) > 6:
                return df.iloc[0:0]
            normalized_query = query_digits.zfill(6)
            for column in selected:
                if column not in df.columns:
                    continue
                normalized = (
                    df[column]
                    .astype(str)
                    .str.replace(r"\.0+$", "", regex=True)
                    .str.replace(r"\D", "", regex=True)
                    .str[-6:]
                    .str.zfill(6)
                )
                mask |= normalized.eq(normalized_query)
            return df.loc[mask]
        for column in selected:
            if column in df.columns: mask |= df[column].astype(str).str.contains(query,case=False,regex=False,na=False)
        return df.loc[mask]

def value(row: pd.Series, column: str, missing: str, maximum: int=300) -> str:
    result=row.get(column, "")
    if pd.isna(result) or not str(result).strip(): return missing
    result=str(result).strip(); return result if len(result)<=maximum else result[:maximum-1].rstrip()+"…"

def hs(value_: str, missing: str) -> str:
    if value_==missing: return value_
    match=re.fullmatch(r"\s*(\d{1,6})(?:\.0+)?\s*",value_)
    return match.group(1).zfill(6) if match else value_
