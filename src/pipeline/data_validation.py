import pandas as pd

class DataValidator:
    def __init__(self, required_columns):
        self.required_columns = required_columns

    def validate_schema(self, df: pd.DataFrame):
        missing = [c for c in self.required_columns if c not in df.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")

    def validate_nulls(self, df: pd.DataFrame):
        if df.isnull().any().any():
            raise ValueError("Null values detected")

    def validate_ranges(self, df: pd.DataFrame, rules: dict):
        for col, (min_v, max_v) in rules.items():
            if col in df.columns:
                if not df[col].between(min_v, max_v).all():
                    raise ValueError(f"Out of range values in {col}")

    def run_all_checks(self, df, range_rules=None):
        self.validate_schema(df)
        self.validate_nulls(df)
        if range_rules:
            self.validate_ranges(df, range_rules)
        return True


import pandas as pd
from dataclasses import dataclass

@dataclass
class MetricResult:
    name: str
    value: any
    metadata: dict = None

class MetricsEngine:
    def run(self, df: pd.DataFrame, kpi_rules=None):
        results = []
        results.append(MetricResult("row_count", len(df)))
        results.append(MetricResult("column_count", df.shape[1]))

        if kpi_rules:
            output = {}
            for k, rule in kpi_rules.items():
                col = rule["column"]
                agg = rule["agg"]
               
