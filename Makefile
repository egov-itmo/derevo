prepare:
	cp frontend/assets/cfg/config.json frontend_config.json
	cp backend/.env.example backend.env

docker-build:
	docker compose build

docker-export: docker-build
	# docker save $(docker compose images | tail -n +2 | awk '{print $1}') -o export/landscaping-images.tar
	docker save landscaping-backend landscaping-frontend landscaping-nginx landscaping-photos -o export/landscaping-images.tar

docker-imprt:
	docker load -i export/landscaping-images.tar
