DOCKER:=@docker
APP_NAME=maissacrement/docker/radio
VERSION=$(shell git rev-parse --short HEAD)
DOCKER_REPO=registry.gitlab.com
xserver_command="gnuradio-companion"

env:=.env
-include $(env)

CRED=
ifdef R_PASS 
ifdef USER
	CRED=--username=${USER} -p ${R_PASS}
endif
endif

login:
	@${DOCKER} login ${DOCKER_REPO} ${CRED} || echo "continue"

xserver:
	${DOCKER} run --rm -it --privileged \
		--env DISPLAY=${DISPLAY} \
		-v /home/Maissacremehnt/.Xauthority:/root/.Xauthority \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
	${APP_NAME} ${xserver_command}

shell:
	@xhost + # Active xhost
	${DOCKER} run --rm -it --privileged \
		--env DISPLAY=${DISPLAY} \
		-v /home/Maissacremehnt/.Xauthority:/root/.Xauthority \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
	${APP_NAME} 

build:
	${DOCKER} build -t ${APP_NAME} .

tag:
	@echo "create tag $(VERSION)"
	${DOCKER} tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):$(VERSION)
	${DOCKER} tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):latest

push: build tag
	${DOCKER} push $(DOCKER_REPO)/$(APP_NAME):$(VERSION)
	${DOCKER} push $(DOCKER_REPO)/$(APP_NAME):latest
