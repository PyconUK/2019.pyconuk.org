help:
	@echo "Usage:"
	@echo "    make help:            prints this help."
	@echo "    make format:          run the auto-format check."
	@echo "    make lint:            run the import sorter check."
	@echo "    make run:             run Django's runserver."
	@echo "    make setup:           set up local env for dev."
	@echo "    make sort             run the linter."

.PHONY: format
format:
	@echo "Running black" && pipenv run black --check pyconuk || exit 1

.PHONY: lint
lint:
	@echo "Running flake8" && pipenv run flake8 --show-source || exit 1

.PHONY: run
run:
	@python manage.py runserver

.PHONY: setup
setup:
	pipenv sync

.PHONY: sort
sort:
	@echo "Running Isort" && pipenv run isort --check-only --diff || exit 1

