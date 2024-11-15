# Variables
SASS_EXEC = sass
PYTHON = python3
SERVER_SCRIPT = run_server.py
CSS_SRC = style.scss
CSS_DEST = assets/stylesheets/output.css
CSS_WATCH_CMD = "CHOKIDAR_USEPOLLING=true sass --watch $(CSS_SRC):$(CSS_DEST)"
PACKAGE_NAME = my_project
VERSION_FILE = version.txt
DIST_DIR = dist

# Phonies : ces cibles ne sont pas des fichiers réels
.PHONY: all clean server css watch version package dependencies

# Cible par défaut
all: css server

# Cible pour compiler le fichier CSS
css: $(CSS_SRC)
	@echo "Compiling SASS to CSS..."
	$(SASS_EXEC) $(CSS_SRC) $(CSS_DEST)

# Cible pour exécuter le serveur
server:
	@echo "Starting the Python HTTP server..."
	$(PYTHON) $(SERVER_SCRIPT)

# Cible pour nettoyer les fichiers générés
clean:
	@echo "Cleaning generated files..."
	rm -f $(CSS_DEST)
	rm -rf $(DIST_DIR)

# Cible pour gérer les dépendances (par exemple installer des bibliothèques nécessaires)
dependencies:
	@echo "Installing system dependencies..."
	./setup_dependencies.sh

# Cible pour incrémenter la version du projet
version:
	@echo "Incrementing project version..."
	@if [ ! -f $(VERSION_FILE) ]; then echo "0.0.1" > $(VERSION_FILE); fi
	@awk -F. '{printf "%d.%d.%d", $$1, $$2, $$3+1}' $(VERSION_FILE) > temp_version && mv temp_version $(VERSION_FILE)
	@echo "New version: $$(cat $(VERSION_FILE))"

# Cible pour packager le projet en un fichier zip
package: clean css
	@echo "Packaging the project..."
	mkdir -p $(DIST_DIR)
	cp -r $(CSS_SRC) $(CSS_DEST) $(SERVER_SCRIPT) $(DIST_DIR)
	cp -r assets $(DIST_DIR)/assets
	echo "Version: $$(cat $(VERSION_FILE))" > $(DIST_DIR)/VERSION
	cd $(DIST_DIR) && zip -r ../$(PACKAGE_NAME)-$$(cat ../$(VERSION_FILE)).zip .
	rm -rf $(DIST_DIR)
	@echo "Project packaged as $(PACKAGE_NAME)-$$(cat $(VERSION_FILE)).zip"


# Cible pour exécuter le script de compilation CSS
compile:
	@echo "Running the CSS compilation script..."
	./compile_css.sh
