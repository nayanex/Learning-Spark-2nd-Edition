notebook:
	jupyter notebook notebooks/

cookie_monster:
	python src/scripts/mnmcount.py data/raw/chapter_2/mnm_dataset.csv

lint:
	poetry run flake8 .

format:
	poetry run black .
	poetry run isort .

typecheck:
	poetry run mypy scripts/

check: format lint typecheck