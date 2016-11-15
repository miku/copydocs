SHELL = /bin/bash

all:
	@echo "Hi!"

index:
	esbulk -purge -index sample -type default -verbose -mapping mapping.v1.json -server http://localhost:9200 sample.ldj
