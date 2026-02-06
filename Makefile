.PHONY: setup run run-win clear clear-win reset

setup:
	python -m venv venv
	mkdir -p ./data
	source ./venv/bin/activate && pip install -r requirements.txt

run:
	source ./venv/bin/activate && uvicorn app.main:app --reload

run-win:
	venv\Scripts\activate && uvicorn app.main:app --reload

reset:
	source ./venv/bin/activate && python -c "from app.db.session import reset_db; reset_db()"
	