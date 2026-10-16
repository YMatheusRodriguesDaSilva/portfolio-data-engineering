.PHONY: setup warehouse dashboard test previews clean

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

warehouse:
	. .venv/bin/activate && python -m src.run_warehouse

dashboard:
	. .venv/bin/activate && streamlit run dashboard/app.py

test:
	. .venv/bin/activate && pytest -q

previews:
	. .venv/bin/activate && python scripts/export_previews.py

clean:
	rm -f data/warehouse/*.db
	rm -f data/raw/*.csv
