# 1. Récupération de l'image Python en version 3.13.1
FROM python:3.13.1-alpine3.21
ARG PORT

# 2. Je vais créer mon système de fichier dans le container
# mkdir /app && cd
WORKDIR /app

# 3. Copier les fichiers de l'application
COPY . .

# 4. Installation des dépendances
RUN pip install --no-cache-dir -r ./requirements.txt

# 5. Le CMD n'appelle pas uvicorn (voir dans main.py)
CMD ["python", "main.py"]
