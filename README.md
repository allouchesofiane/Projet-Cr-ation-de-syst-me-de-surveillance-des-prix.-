# Projet : Création d'un système de surveillance des prix

Ce projet est un **système de surveillance des prix** pour le site [Books to Scrape](https://books.toscrape.com/).  
Il utilise Python pour **extraire, transformer et charger (ETL)** les données des livres.

## Objectifs

- **Phase 1** : Extraire les informations d’un seul livre.
- **Phase 2** : Extraire les informations de tous les livres d’une catégorie.
- **Phase 3** : Extraire les informations de toutes les catégories du site.
- **Phase 4** : Télécharger et sauvegarder les images des couvertures de livres.

## Mise en place de l’environnement

### 1. Créer un environnement virtuel (Windows)
python -m venv env

### 2. Activer l’environnement virtuel

env\Scripts\activate.ps1

### 3. Installer les dépendances
pip install -r requirements.txt

### 4. Gestion du .gitignore
À ne pas versionner :

Environnement virtuel : env/

Fichiers CSV générés : *.csv

Images téléchargées : /images/, *.png, *.jpg, etc.

## Phases du projet

### Phase 1 : Extraire les informations d’un seul livre
Scrape les données d’un seul produit.

Sauvegarde dans product_data.csv.

#### Champs extraits :

product_page_url

universal_product_code (UPC)

title

price_including_tax

price_excluding_tax

number_available

product_description

category

review_rating

image_url

### Phase 2 : Extraire les livres d’une catégorie
Scrape tous les livres d’une catégorie précise.

Gère la pagination automatique.

Enregistre les données dans un fichier CSV par catégorie.

### Phase 3 : Extraire toutes les catégories

Récupère les URL de toutes les catégories du site.

Scrape les livres de chaque catégorie.

Crée un CSV distinct par catégorie.

### Phase 4 : Télécharger les images

Pour chaque livre, télécharge l’image de couverture.

Enregistre les images dans le dossier images/.

## Exécution
Lance ce projet avec une seule commande :

python main.py

##  Dépendances utilisées
requests

beautifulsoup4

lxml

urllib.parse

csv

os
