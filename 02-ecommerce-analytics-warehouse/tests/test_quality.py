from __future__ import annotations

import sqlite3

from src.data_quality import run_checks
from src.run_warehouse import run


def test_warehouse_quality_gates():
    db = run()
    assert db.exists()
    with sqlite3.connect(db) as conn:
        results = run_checks(conn)
    assert results
    assert all(r.passed for r in results)
