sh:
	docker exec -it microservices_mr_sandwich_web_store_cart bash

envs:
	docker exec -it microservices_mr_sandwich_web_store_cart printenv

dev:
	uvicorn main:app --reload --port 8002 --log-level info --debug

generate-migration:
	cd _migrations && alembic revision --autogenerate -m "${m}"

migrate:
	cd _migrations && alembic upgrade head
