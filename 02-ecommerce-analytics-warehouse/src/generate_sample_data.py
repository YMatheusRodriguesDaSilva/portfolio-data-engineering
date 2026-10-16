"""Generate sample e-commerce transactional extracts."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"


def generate(n_customers: int = 120, n_orders: int = 400, seed: int = 21) -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)

    customers = pd.DataFrame(
        {
            "customer_id": range(1, n_customers + 1),
            "full_name": [f"Customer {i}" for i in range(1, n_customers + 1)],
            "email": [f"customer{i}@example.com" for i in range(1, n_customers + 1)],
            "city": rng.choice(["São Paulo", "Rio de Janeiro", "Curitiba", "Belo Horizonte"], n_customers),
            "state": rng.choice(["SP", "RJ", "PR", "MG"], n_customers),
            "created_at": [
                (datetime(2025, 1, 1) + timedelta(days=int(x))).strftime("%Y-%m-%d")
                for x in rng.integers(0, 400, n_customers)
            ],
        }
    )

    products = pd.DataFrame(
        {
            "product_id": [1, 2, 3, 4, 5, 6],
            "product_name": [
                "Running Shoes",
                "Casual Sneaker",
                "Leather Bag",
                "Sports Sandal",
                "Winter Boot",
                "Canvas Tote",
            ],
            "category": ["Footwear", "Footwear", "Bags", "Footwear", "Footwear", "Bags"],
            "unit_price": [249.9, 189.9, 319.0, 129.5, 399.0, 99.0],
        }
    )

    start = datetime(2026, 7, 1)
    orders = pd.DataFrame(
        {
            "order_id": range(1, n_orders + 1),
            "customer_id": rng.integers(1, n_customers + 1, n_orders),
            "order_date": [
                (start + timedelta(days=int(x))).strftime("%Y-%m-%d")
                for x in rng.integers(0, 90, n_orders)
            ],
            "status": rng.choice(
                ["paid", "shipped", "delivered", "cancelled"],
                n_orders,
                p=[0.35, 0.30, 0.25, 0.10],
            ),
        }
    )

    items_rows = []
    item_id = 1
    price_map = dict(zip(products["product_id"], products["unit_price"]))
    for order_id in orders["order_id"]:
        for product_id in rng.choice(products["product_id"], size=int(rng.integers(1, 4)), replace=False):
            qty = int(rng.integers(1, 4))
            items_rows.append(
                {
                    "order_item_id": item_id,
                    "order_id": int(order_id),
                    "product_id": int(product_id),
                    "quantity": qty,
                    "unit_price": float(price_map[int(product_id)]),
                }
            )
            item_id += 1
    order_items = pd.DataFrame(items_rows)

    customers.to_csv(RAW / "customers.csv", index=False)
    products.to_csv(RAW / "products.csv", index=False)
    orders.to_csv(RAW / "orders.csv", index=False)
    order_items.to_csv(RAW / "order_items.csv", index=False)
    print(f"Sample raw data written to {RAW}")


if __name__ == "__main__":
    generate()
