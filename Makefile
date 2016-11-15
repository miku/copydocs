SHELL = /bin/bash

all:
	@echo "Hi!"

sample.ldj:
	# turn HTML from wiki into JSON
	python pp.py > sample.ldj

clean:
	rm -f sample.ldj

index:
	# TODO: adjust mapping
	esbulk -purge -index sample -type default -verbose -mapping mapping.v1.json -server http://localhost:9200 sample.ldj
