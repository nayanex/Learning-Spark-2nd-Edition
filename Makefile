notebook:
	jupyter notebook notebooks/

lint:
	poetry run flake8 .

format:
	poetry run black .
	poetry run isort .

typecheck:
	poetry run mypy scripts/

check: format lint typecheck