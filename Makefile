DOCKER:=@docker
APP_NAME=radio
xserver_command="gnuradio-companion"

env:=.env
-include $(env)

xserver:
	${DOCKER} run --rm -it --privileged \
		--env DISPLAY=${DISPLAY} \
		-v /home/Maissacremehnt/.Xauthority:/root/.Xauthority \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
	${APP_NAME} ${xserver_command}

shell:
	${DOCKER} run --rm -it --privileged \
		--env DISPLAY=${DISPLAY} \
		-v /home/Maissacremehnt/.Xauthority:/root/.Xauthority \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
	${APP_NAME}

build:
	${DOCKER} build -t ${APP_NAME} .


