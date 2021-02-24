TARBALL := dist/ginkgo-bioworks-tech-assessment.docker.tar
IMAGE_NAME := docker.11x.engineering/ginkgo-bioworks-tech-assessment:latest
FRONTEND_BUILD_COMMAND := npm install && yarn build

# Paths to TLS certificates for your local dev machine.
TLS_PRIVATE_KEY := $(shell pwd)/infrastructure/key.local.pem
TLS_CERTIFICATE_CHAIN := $(shell pwd)/infrastructure/chain.local.pem

DEV_KEY_VOLUME_MAPPING := ${TLS_PRIVATE_KEY}:/srv/certificates/key.pem
DEV_CHAIN_VOLUME_MAPPING := ${TLS_CERTIFICATE_CHAIN}:/srv/certificates/crt.pem

DEV_TLS_VOLUME_MAPPINGS := -v ${DEV_KEY_VOLUME_MAPPING} -v ${DEV_CHAIN_VOLUME_MAPPING}
DEV_DATABASE_VOLUME_MAPPING := -v $$(pwd)/db.sqlite3:/app/db.sqlite3
DEV_MEDIA_VOLUME_MAPPING := -v $$(pwd)/media:/srv/media


SOURCES := conf/*.py \
           jobs/*.py \
           protein_search/*.py \
           manage.py

DOCKER_SOURCES := deployment/* \
                  Dockerfile \
                  .dockerignore \
                  requirements.txt

FRONTEND_SOURCES := frontend/src/*.js \
                    frontend/src/*.css \
                    frontend/public/*

FRONTEND_INDEX_TARGET := frontend/static/index.html


.PHONY: quick clean image


vars:
	@echo TLS_PRIVATE_KEY = ${TLS_PRIVATE_KEY}
	@echo TLS_CERTIFICATE_CHAIN = ${TLS_CERTIFICATE_CHAIN}
	@echo SOURCES = ${SOURCES}
	@echo DOCKER_SOURCES = ${DOCKER_SOURCES}


clean:
	-rm -rf dist/


image: ${TARBALL}


${TARBALL}: ${SOURCES} ${DOCKER_SOURCES} ${FRONTEND_INDEX_TARGET}
	mkdir -p dist
	docker build -t ${IMAGE_NAME} .
	docker save --output ${TARBALL} ${IMAGE_NAME}


${FRONTEND_INDEX_TARGET}: ${FRONTEND_SOURCES}
	cd frontend && ${FRONTEND_BUILD_COMMAND}


quick: ${FRONTEND_INDEX_TARGET}
	docker build -t ${IMAGE_NAME} .
	docker-compose -f docker-compose.dev.yml up
