down:
	docker kill $(docker ps --filter "name=ocean" -q)
	
start:
	./start.sh

restart:
	docker kill $(docker ps --filter "name=ocean" -q); ./start.sh;


prune_volumes:	
	docker system prune --all --volumes
bash:
	docker exec -it ${arg} bash

build_backend:
	docker-compose -f "backend/backend.yml" build;