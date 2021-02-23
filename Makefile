TARBALL := dist/ginkgo-bioworks-tech-assessment.docker.tar
IMAGE_NAME := docker.11x.engineering/ginkgo-bioworks-tech-assessment:latest
PYTHON := .v/bin/python

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

.PHONY: quick clean image


vars:
	@echo TLS_PRIVATE_KEY = ${TLS_PRIVATE_KEY}
	@echo TLS_CERTIFICATE_CHAIN = ${TLS_CERTIFICATE_CHAIN}
	@echo SOURCES = ${SOURCES}
	@echo DOCKER_SOURCES = ${DOCKER_SOURCES}


clean:
	-rm -rf dist/


image: ${TARBALL}


${TARBALL}: ${SOURCES} ${DOCKER_SOURCES}
	mkdir -p dist
	docker build -t ${IMAGE_NAME} .
	docker save --output ${TARBALL} ${IMAGE_NAME}


quick:
	docker build -t ${IMAGE_NAME} .
	docker run --rm --name ginkgo-bioworks-tech-assessment \
	                -p 80:80 \
	                -p 443:443 \
	                ${DEV_DATABASE_VOLUME_MAPPING} \
	                ${DEV_TLS_VOLUME_MAPPINGS} \
	                ${DEV_MEDIA_VOLUME_MAPPING} \
	                -e DJANGO_SETTINGS_MODULE=conf.settings \
	                    ${IMAGE_NAME}
