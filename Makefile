ifneq (,$(wildcard ./.env))
   include .env
   export
   ENV_FILE_PARAM = --env-file .env
endif

build:
	docker-compose up --build --remove-orphans

up:
	docker-compose up

down:
	docker-compose down

migrate:
	docker-compose exec logistic python3 manage.py migrate --noinput

makemigrations:
	docker-compose exec logistic python3 manage.py makemigrations

superuser:
	docker-compose exec logistic python3 manage.py createsuperuser

down-v:
	docker-compose down -v

volume:
	docker volume inspect cvrp_postgres_data

shell:
	docker exec exec logistic python3 manage.py shell