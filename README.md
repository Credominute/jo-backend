# 🏅Projet Python - Jeux Olympiques 2024

Ce projet est une API REST développée avec FastAPI des JO et utilise le langage Python. 
Ce manuel va vous aider à configurer et à exécuter cette application en local.

## 🛠️ Prérequis

Avant de commencer, assurez-vous d'avoir installé l'élément suivant sur votre machine :

- [Python 3.13.1 ou supérieur](https://www.python.org/downloads/)

## 📦 Installation

1. Clonez le dépôt :
    ```bash
    git clone https://github.com/Credominute/jo-backend.git
    ```
2. Créer et activer un environnement virtuel
    ```bash
   python -m venv venv
   ```
   
3. Installez les dépendances :
    ```bash
    python -m pip install -r ./requirements.txt
    ```
    
## ▶️ Exécution en Local

1. Démarrez le serveur de développement :
   ```bash
   python -m uvicorn main:app --reload
   ```
soit accédez à l'API Swagger UI http://127.0.0.1:8000/docs
soit au front Angular en local avec http://localhost:4200/

2. Tests avec couverture
   ```bash
   coverage run -m pytest
   ```
Ce qui lance les tests avec la collecte de la couverture, dont le rapport est finalement fourni par : 
   ```bash
   coverage report -m
   ```

