# Projet Python - Jeux Olympiques 2024

Ce projet des JO est une application Python pour une API. Ce manuel va vous aider à configurer et à exécuter cette application en local.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé l'élément suivant sur votre machine :

- [Python 3.13.1 ou supérieur](https://www.python.org/downloads/)

## Installation

1. Créer un environnement virtuel et l'activer

2. Clonez le dépôt :
    ```bash
    git clone https://github.com/Credominute/jo-backend.git
    ```

3. Installez les dépendances :
    ```bash
    python pip3 install -r ./requirements.txt
    ```
    
## Exécution en Local

1. Démarrez le serveur de développement :
   Lancer l'application avec `python -m uvicorn main:app --reload` et se rendre à [http://localhost:4200/](http://127.0.0.1:8000)

2. Aide technique :
   Ce projet utilise les librairies SQLAlchemy, PyTest, python-jose (JWT), l'IDE se connecte à une base de données PostgreSQL
