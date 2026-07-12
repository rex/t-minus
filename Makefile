.PHONY: run stop open

PORT := 4173

run: ## serve T-MINUS with the native say voice at http://localhost:4173
	python3 serve.py

open: ## open the app in the default browser
	open http://localhost:$(PORT)

stop: ## kill anything listening on the port
	-@lsof -ti tcp:$(PORT) | xargs kill 2>/dev/null; true
	@echo "port $(PORT) clear"
