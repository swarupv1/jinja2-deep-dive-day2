NAME = "netdev/tools"
VERSION = "0.1"

.PHONY: container run clean-images clean-stopped
default: container


container:
	docker build -t $(NAME):$(VERSION) .

run:
	docker run -it $(NAME):$(VERSION)

clean-images:
	docker image rm -f $(NAME):$(VERSION)

clean-stopped:
	docker container prune -f
