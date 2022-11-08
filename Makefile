DOCKER:=@docker
APP_NAME=maissacrement/docker/radio
VERSION=$(shell git rev-parse --short HEAD)
DOCKER_REPO=registry.gitlab.com
PWD:=`pwd`

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

build:
	${DOCKER} build -t ${APP_NAME} . --file ./docker/gnuradio.Dockerfile

xserver-dev: build
	xhost + # give foward auth
	${DOCKER} run --rm -it --privileged \
		--env DISPLAY=${DISPLAY} \
		-v $(HOME)/.Xauthority:/root/.Xauthority \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		-v ${PWD}/grc:/opt/gr-wban \
		-v /dev/bus/usb:/dev/bus/usb \
	${APP_NAME} /bin/bash -c "entrypoint.sh"
	xhost -

shell: build
	xhost +
	${DOCKER} run --rm -it --privileged \
		--env DISPLAY=${DISPLAY} \
		-v $(HOME)/.Xauthority:/root/.Xauthority \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		-v $(PWD)/grc:/opt/gr-wban \
		-v /dev/bus/usb:/dev/bus/usb \
	${APP_NAME}
	xhost -

tag:
	@echo "create tag $(VERSION)"
	${DOCKER} tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):$(VERSION)
	${DOCKER} tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):latest

push: login build tag
	${DOCKER} push $(DOCKER_REPO)/$(APP_NAME):$(VERSION)
	${DOCKER} push $(DOCKER_REPO)/$(APP_NAME):latest

pull:
	${DOCKER} pull $(DOCKER_REPO)/$(APP_NAME):latest

xserver: pull
	xhost + # give foward auth
	${DOCKER} run --rm -it --privileged \
				--user "$(id -u):$(id -g)" \
                --env DISPLAY=${DISPLAY} \
                -v $(HOME)/.Xauthority:/root/.Xauthority \
                -v /tmp/.X11-unix:/tmp/.X11-unix \
                -v ${PWD}/grc:/opt/gr-wban \
                -v /dev/bus/usb:/dev/bus/usb \
        $(DOCKER_REPO)/$(APP_NAME):latest /bin/bash -c "entrypoint.sh"
	xhost -


