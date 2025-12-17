"""
Metrics Engine Module
---------------------
Computes repeatable analytics metrics from validated datasets.
Designed for automated reporting workflows.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
import pandas as pd


@dataclass
class MetricResult:
    name: str
    value: Any
    metadata: Optional[Dict[str, Any]] = None


class MetricsEngine:
    def __init__(self):
        self.results = []

    def compute_row_count(self, df: pd.DataFrame) -> MetricResult:
        return MetricResult(name="row_count", value=int(len(df)))

    def compute_column_count(self, df: pd.DataFrame) -> MetricResult:
        return MetricResult(name="column_count", value=int(df.shape[1]))

    def compute_custom_kpis(
        self, df: pd.DataFrame, kpi_rules: Dict[str, Dict[str, str]]
    ) -> MetricResult:
        output = {}
        for kpi_name, rule in kpi_rules.items():
            col = rule.get("column")
            agg = rule.get("agg")

            if col not in df.columns:
                output[kpi_name] = {"error": f"missing column '{col}'"}
                continue

            if agg == "sum":
                output[kpi_name] = float(df[col].sum())
            elif agg == "mean":
                output[kpi_name] = float(df[col].mean())
            elif agg == "max":
                output[kpi_name] = float(df[col].max())
            else:
                output[kpi_name] = {"error": f"unsupported agg '{agg}'"}

        return MetricResult(name="custom_kpis", value=output)

    def run(
        self,
        df: pd.DataFrame,
        kpi_rules: Optional[Dict[str, Dict[str, str]]] = None,
    ):
        self.results = []
        self.results.append(self.compute_row_count(df))
        self.results.append(self.compute_column_count(df))

        if kpi_rules:
            self.results.append(self.compute_custom_kpis(df, kpi_rules))

        return self.results

