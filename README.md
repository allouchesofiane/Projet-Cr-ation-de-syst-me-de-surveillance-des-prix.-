# Projet : Creation d'un systeme de surveillance des prix.
Ce projet est un **système de surveillance des prix** pour le site [Books to Scrape](https://books.toscrape.com/)
Il utilise Python pour **extraire, transformer et charger (ETL)** les données des livres

## Objectifs des phases

- **Phase 1 :** Extraire les informations d’un seul livre.
- **Phase 2 :** Extraire les informations de tous les livres d’une catégorie.
- **Phase 3 :** Extraire les informations de toutes les catégories du site.
- **Phase 4 :** Télécharger et sauvegarder les images des couvertures de livres.

## Créer un environnement virtuel
### Sous Windows
**script** python -m venv env

### Activation de l’environnement virtuel
**script** env\Scripts\activate

### Les dépendances
Tous les modules nécessaires (requests, BeautifulSoup, etc.) sont listés dans le fichier requirements.txt.
**script** pip install -r requirements.txt

### Gestion .gitignore
Ne committez pas :
#### Environnement virtuel
env/
#### CSV générés
*.csv
#### Images téléchargées
/images/
*.png
*.jpg
*.jpeg
*.gif
*.bmp
*.svg
*.webp

## Phases du projet

### Phase 1 : Extraire les informations d’un seul livre.
#### Objectif
Ce script scrape les informations détaillées d’un **seul livre** depuis le site [Books to Scrape](https://books.toscrape.com).

#### Données extraites
- `product_page_url`
- `universal_product_code (upc)`
- `title`
- `price_including_tax`
- `price_excluding_tax`
- `number_available`
- `product_description`
- `category`
- `review_rating`
- `image_url`
Les données sont stockées dans un fichier CSV appelé `product_data.csv`.

#### Dépendances
- `requests`
- `beautifulsoup4`
- `lxml`
- `urllib.parse`
- `csv`

## Exécution
python product_data.py

### Phase 2 : Extraire les informations de tous les livres d’une catégorie.
#### Objectif
Ce script scrape **tous les livres d'une catégorie** spécifique sur le site Books to Scrape. Il gère aussi la **pagination automatique** si la catégorie contient plusieurs pages.

#### Fonctionnement
1️⃣ Le script récupère la liste des livres d'une catégorie.  
2️⃣ Il extrait les détails de chaque livre.  
3️⃣ Les données sont enregistrées dans un **fichier CSV unique** pour la catégorie.

#### Exemple de données extraites
- `product_page_url`
- `universal_product_code (upc)`
- `title`
- `price_including_tax`
- `price_excluding_tax`
- `number_available`
- `product_description`
- `category`
- `review_rating`
- `image_url`

#### Dépendances
- `requests`
- `beautifulsoup4`
- `lxml`
- `urllib.parse`
- `csv`

## Exécution
python category_data.py

### Phase 3 : Extraire les informations de toutes les catégories du site.
## Objectif
Ce script scrape **toutes les catégories** du site Books to Scrape et enregistre les détails des livres dans un fichier CSV **par catégorie**.

## Fonctionnement
- Pour chaque catégorie :
  - Il récupère tous les liens de livres (gestion automatique des pages multiples).
  - Il scrape les informations détaillées de chaque livre.
  - Les données sont stockées dans un fichier CSV au nom de la catégorie.

#### Dépendances
- `requests`
- `beautifulsoup4`
- `lxml`
- `urllib.parse`
- `csv`

## Exécution
python all_categories_data.py

### Phase 4 :Télécharger et sauvegarder les images des couvertures de livres. 
## Objectif
Ce script  **extrait et télécharge les images** de chaque livre en local.

## Fonctionnement
- **Téléchargement des images** : chaque image est enregistrée dans un dossier `images/` avec un nom basé sur le **titre** + **UPC**.

## Données extraites

- `product_page_url`
- `universal_product_code (upc)`
- `title`
- `price_including_tax`
- `price_excluding_tax`
- `number_available`
- `product_description`
- `category`
- `review_rating`
- `image_url`

#### Dépendances
- `requests`
- `beautifulsoup4`
- `lxml`
- `urllib.parse`
- `csv`
- `os`
- `re`

## Exécution
python python all_categories_data.py