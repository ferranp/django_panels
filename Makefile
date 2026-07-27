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
	git push origin main

.PHONY: deploy_test
deploy_test:
	git push origin main
