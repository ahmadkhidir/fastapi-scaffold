SHELL := /bin/bash  # Ensures a consistent shell (Linux and Git Bash on Windows)

db-migrations:
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "Error: Migration comment is required"; \
		exit 1; \
	fi
	@echo "Generating migration script"
	docker compose exec server sh -c 'alembic -c alembic.ini revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"'
	@echo "Migration script generated"

db-migrate:
	@echo "Applying migration script"
	docker compose exec server sh -c 'alembic -c alembic.ini upgrade head'
	@echo "Migration script applied"

db-update:
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "Error: Migration comment is required"; \
		exit 1; \
	fi
	@echo "Updating models"
	$(MAKE) db-migrations "$(filter-out $@,$(MAKECMDGOALS))"
	$(MAKE) db-migrate
	@echo "Models updated"

# Prevents make from interpreting the comment as a target
%:
	@:
