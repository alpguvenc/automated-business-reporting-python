from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import requests


@dataclass(frozen=True)
class SalesFetchParams:
    start_date: str  # YYYY-MM-DD
    end_date: str    # YYYY-MM-DD


def fetch_sales_data(
    *,
    base_url: str,
    api_key: str,
    timeout_seconds: int,
    params: SalesFetchParams,
) -> list[dict[str, Any]]:
    """
    Expected API response example:
    [
        {
            "order_id": "A1001",
            "order_date": "2025-12-01",
            "customer_id": "C10",
            "country": "US",
            "channel": "web",
            "product": "Backpack",
            "quantity": 1,
            "unit_price": 79.99,
            "discount": 5.00,
            "shipping": 0.00
        }
    ]
    """
    url = f"{base_url.rstrip('/')}/sales"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }
    query = {
        "start_date": params.start_date,
        "end_date": params.end_date,
    }

    response = requests.get(
        url,
        headers=headers,
        params=query,
        timeout=timeout_seconds,
    )
    response.raise_for_status()

    data = response.json()
    if not isinstance(data, list):
        raise ValueError("Unexpected API response format")

    return data
