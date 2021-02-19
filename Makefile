VERSION = `git rev-parse --short HEAD`
TO := _
SKIP_SLEEP ?= 0

ifdef BUILD_NUMBER
NUMBER = $(BUILD_NUMBER)
else
NUMBER = 1
endif

ifdef JOB_BASE_NAME
PROJECT_ENCODED_SLASH = $(subst %2F,$(TO),$(JOB_BASE_NAME))
PROJECT = $(subst /,$(TO),$(PROJECT_ENCODED_SLASH))
# Run on CI
COMPOSE = docker-compose -f docker-compose.yml -f docker-compose.ci.yml -p kafka_streamprocessor_$(PROJECT)_$(NUMBER)
else
# Run Locally
COMPOSE = docker-compose -p kafka_streamprocessor
endif

.PHONY: init
init:
	# This following command is used to provision the network
	$(COMPOSE) up --no-start --no-build app | true

.PHONY: run
run:
	#alfred project secrets import
	$(COMPOSE) build app
	$(COMPOSE) up app



.PHONY: down
down:
	$(COMPOSE) down --volumes


.PHONY: format
format:
	$(COMPOSE) build format-imports
	$(COMPOSE) run format-imports
	$(COMPOSE) build format
	$(COMPOSE) run format


.PHONY: check-format
check-format:
	$(COMPOSE) build check-format-imports
	$(COMPOSE) run check-format-imports
	$(COMPOSE) build check-format
	$(COMPOSE) run check-format


.PHONY: style
style: check-format
	$(COMPOSE) build style
	$(COMPOSE) run style


.PHONY: complexity
complexity:
	$(COMPOSE) build complexity
	$(COMPOSE) run complexity

.PHONY: test-unit
test-unit:
	$(COMPOSE) build test-unit
	$(COMPOSE) run test-unit


.PHONY: test
test: test-unit


.PHONY: security-sast
security-sast:
	$(COMPOSE) build security-sast
	$(COMPOSE) run security-sast
