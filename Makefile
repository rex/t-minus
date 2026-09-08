.PHONY: run start stop open status

PORT := 4173
LOG  := $(HOME)/Library/Logs/t-minus.log
UID  := $(shell id -u)

run: ## serve T-MINUS with the native say voice at http://localhost:4173
	python3 serve.py

open: ## open the app in the default browser
	open http://localhost:$(PORT)

start: ## same, but detached — survives closing the terminal (stop with: make stop)
	@nohup python3 serve.py >> $(LOG) 2>&1 & sleep 1
	@curl -sf http://localhost:$(PORT)/ping >/dev/null \
		&& echo "T-MINUS up · http://localhost:$(PORT) · log: $(LOG)" \
		|| { echo "failed to start — see $(LOG)"; exit 1; }

stop: ## stop the server, and make sure the time-announcer is back on
	-@lsof -ti tcp:$(PORT) | xargs kill 2>/dev/null; true
	@sleep 1
	-@launchctl enable gui/$(UID)/com.pierce.time-announcer 2>/dev/null; true
	@echo "port $(PORT) clear · time-announcer enabled"

status: ## is T-MINUS up, and is the time-announcer paused?
	@lsof -ti tcp:$(PORT) >/dev/null 2>&1 \
		&& echo "T-MINUS       : RUNNING  http://localhost:$(PORT)" \
		|| echo "T-MINUS       : stopped"
	@launchctl print-disabled gui/$(UID) 2>/dev/null | grep time-announcer | grep -qiE 'true|disabled' \
		&& echo "time-announcer: PAUSED" \
		|| echo "time-announcer: active (speaks on :00 and :30)"
