down:
	docker kill $(docker ps --filter "name=ocean")
start:
	./start.sh
prune_volumes:	
	docker system prune --all --volumes
bash:
	docker exec -it ${arg} bash