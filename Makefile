# Makefile for intranet quality chemicals
#

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  clean       to delete generated icons"


.PHONY: clean
clean:
	rm ${ICONS}

.PHONY: deploy
deploy:
	hg bookmark -r default master ; hg push

.PHONY: deploy_test
deploy_test:
	hg bookmark -r default master ; hg push
