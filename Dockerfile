# 1. Récupération de l'image Python (dernière version : 3.13.2)
FROM python:3.13.1-alpine3.21
ARG PORT

# 2. Création du répertoire de fichier dans le container
WORKDIR /app

# 3. Copie de tous les fichiers de mon application
COPY . .

# 4. Installation de mes dépendances (-r: reccurssif)
RUN pip install --no-cache-dir -r ./requirements.txt

# 5. Heroku execute main et lance son propre serveur
CMD ["python", "main.py"]
