from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "customer_id",
    "country",
    "channel",
    "product",
    "quantity",
    "unit_price",
    "discount",
    "shipping",
]


def to_dataframe(raw_rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(raw_rows)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns from API payload: {missing}")

    # Parse types
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    for c in ["quantity", "unit_price", "discount", "shipping"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # Drop broken rows
    df = df.dropna(subset=["order_id", "order_date", "quantity", "unit_price"])

    # Business logic
    df["gross_revenue"] = df["quantity"] * df["unit_price"]
    df["net_revenue"] = df["gross_revenue"] - df["discount"].fillna(0) + df["shipping"].fillna(0)

    # Normalize text fields
    for c in ["country", "channel", "product"]:
        df[c] = df[c].astype(str).str.strip()

    return df


def build_kpis(df: pd.DataFrame) -> dict[str, float]:
    total_orders = float(df["order_id"].nunique())
    total_customers = float(df["customer_id"].nunique())
    total_net_revenue = float(df["net_revenue"].sum())
    avg_order_value = float(total_net_revenue / total_orders) if total_orders else 0.0

    return {
        "total_orders": total_orders,
        "total_customers": total_customers,
        "total_net_revenue": total_net_revenue,
        "avg_order_value": avg_order_value,
    }


def revenue_by_day(df: pd.DataFrame) -> pd.DataFrame:
    out = (
        df.assign(day=df["order_date"].dt.date)
          .groupby("day", as_index=False)["net_revenue"].sum()
          .sort_values("day")
    )
    return out


def revenue_by_channel(df: pd.DataFrame) -> pd.DataFrame:
    out = (
        df.groupby("channel", as_index=False)["net_revenue"].sum()
          .sort_values("net_revenue", ascending=False)
    )
    return out


def top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    out = (
        df.groupby("product", as_index=False)["net_revenue"].sum()
          .sort_values("net_revenue", ascending=False)
          .head(n)
    )
    return out
