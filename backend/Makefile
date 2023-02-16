VERSION = 0.1.0

DOCKER_USER_WITH_SLASH = 

lint:
	pylint plants_api --max-line-length 120

run:
	python -m plants_api

debug:
	python -m plants_api --debug

docker-build:
	docker build --tag $(DOCKER_USER_WITH_SLASH)plants_api:$(VERSION) .

docker-run:
	docker run --env-file .env --rm --name plants_api

docker-push:
	docker push $(DOCKER_USER_WITH_SLASH)plants_api:$(VERSION)

docker-update-latest:
	docker tag $(DOCKER_USER_WITH_SLASH)plants_api:$(VERSION) $(DOCKER_USER_WITH_SLASH)plants_api:latest
	docker push $(DOCKER_USER_WITH_SLASH)plants_api:latest

docker-pipeline: docker-build docker-push docker-update-latest

db-revision:
	cd plants_api/db && alembic revision --autogenerate

db-migrate:
	cd plants_api/db && alembic upgrade head