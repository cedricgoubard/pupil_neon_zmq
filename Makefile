build:
	docker build -t pupil_zmq .


test: CMD_AND_ARGS="python -m pupilzmq --cfg /work/cfg.yaml"
test: .run

.run:
	docker run \
		-it \
		--rm \
		-v $(shell pwd):/work \
		--net=host \
		--name pupil_zmq \
		pupil_zmq bash -c $(CMD_AND_ARGS)