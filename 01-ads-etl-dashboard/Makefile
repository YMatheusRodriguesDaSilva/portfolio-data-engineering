.PHONY: setup pipeline dashboard test previews clean

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

pipeline:
	. .venv/bin/activate && python -m src.pipeline

pipeline-reuse:
	. .venv/bin/activate && python -m src.pipeline --skip-generate

dashboard:
	. .venv/bin/activate && streamlit run dashboard/app.py

test:
	. .venv/bin/activate && pytest -q

previews:
	. .venv/bin/activate && python scripts/export_previews.py

clean:
	rm -f data/processed/warehouse.db
	rm -f data/raw/*.csv
