.PHONY: setup pipeline dashboard test clean

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

clean:
	rm -f data/processed/warehouse.db
	rm -f data/raw/*.csv
