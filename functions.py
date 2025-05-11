import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os

BASE_URL = 'https://books.toscrape.com/'

def fetch_page(url):
    """Télécharge la page web et retourne l'objet BeautifulSoup."""
    response = requests.get(url)
    if response.ok:
        return BeautifulSoup(response.text, 'lxml')
    else:
        print("Erreur lors de la récupération de la page")
        return None

def parse_product_data(soup, url):
    """Extrait toutes les données produit sous forme de dictionnaire."""
    title = soup.find('h1').text.strip()
    table = soup.find('table', class_='table table-striped')
    rows = table.find_all('tr')
    data = {}
    for row in rows:
        key = row.th.text.strip()
        value = row.td.text.strip()
        data[key] = value
        print(data)
    universal_product_code = data.get('UPC')
    price_including_tax = data.get('Price (incl. tax)')
    price_excluding_tax = data.get('Price (excl. tax)')
    number_available = data.get('Availability')
    description_block = soup.find('article', class_='product_page')
    product_description = description_block.find_all('p')[3].text.strip() if description_block else ''
    category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
    image_relative_url = soup.find('img')['src']
    image_url = urljoin(url, image_relative_url)
    return {
        'product_page_url': url,
        'universal_product_code': universal_product_code,
        'title': title,
        'price_including_tax': price_including_tax,
        'price_excluding_tax': price_excluding_tax,
        'number_available': number_available,
        'product_description': product_description,
        'category': category,
        'image_url': image_url
    }

def get_review_rating(soup):
    """Cherche le nombre d'étoiles et retourne un chiffre (1 à 5)."""
    
    # Cherche la balise qui indique la note :
    star_tag = soup.find('p', class_='star-rating')
    
    # Récupère la liste des classes CSS (par exemple ['star-rating', 'Three'])
    if star_tag:
        classes = star_tag.get('class')
    else:
        classes = []

    # Essaie de prendre la 2e classe (qui contient la note : 'One', 'Two', ...)
    if len(classes) > 1:
        star_text = classes[1]
    else:
        star_text = ''

    # Prépare le dictionnaire pour traduire le mot en chiffre :
    stars_dict = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    #Retourne le chiffre correspondant, ou 0 si on ne trouve pas :
    return stars_dict.get(star_text)

def save_to_csv(data, csv_file):
    """Sauvegarde les données dans un fichier CSV."""
    headers = ['product_page_url', 'universal_product_code', 'title',
               'price_including_tax', 'price_excluding_tax',
               'number_available', 'product_description',
               'category', 'review_rating', 'image_url']
    
    with open(csv_file, 'w', encoding='UTF8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()  # écrit les titres des colonnes

        # Vérifie si c'est une liste ou un dict
        if isinstance(data, list):
            # Boucle sur chaque dictionnaire
            for row in data:
                writer.writerow(row)
        elif isinstance(data, dict):
            # Écrit directement si c'est un dict unique
            writer.writerow(data)
        else:
            print("Erreur : format des données non reconnu.")

def get_all_categories(base_url=BASE_URL):
    """Récupère tous les liens des catégories à partir de la page d'accueil."""
    categories = {}
    soup = fetch_page(base_url)
    if not soup:
        return categories
    
    category_section = soup.find('ul', class_='nav-list')
    category_links = category_section.find_all('a')

    for link in category_links:
        category_name = link.text.strip()
        relative_url = link.get('href')
        category_url = urljoin(base_url, relative_url)
        #On ignore la première catégorie “Books” qui n’en est pas vraiment une
        if category_name.lower() != 'books':
            categories[category_name] = category_url
    #Elle retourne un dictionnaire avec les noms comme clés et les URLs comme valeurs.
    return categories

def get_all_book_links(category_url):
    """Récupère tous les liens des livres d'une catégorie (pagination comprise)."""
    book_links = []
    while category_url:
        soup = fetch_page(category_url)
        if not soup:
            break
        
        articles = soup.find_all('article', class_='product_pod')
        for article in articles:
            a_tag = article.find('h3').find('a')
            relative_url = a_tag['href']
            book_url = urljoin(category_url, relative_url)
            book_links.append(book_url)

        next_button = soup.find('li', class_='next')
        if next_button:
            next_page = next_button.find('a')['href']
            category_url = urljoin(category_url, next_page)
        else:
            category_url = None

    return book_links

def download_image(image_url, save_folder='images'):
    """Télécharge l'image depuis image_url et la sauvegarde dans le dossier choisi."""
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    # On récupère le nom du fichier image à partir de son URL
    filename = image_url.split('/')[-1]
    #On **crée le chemin complet** où l’image sera enregistrée
    filepath = os.path.join(save_folder, filename)

    response = requests.get(image_url, stream=True)
    if response.ok:
        #On ouvre le fichier en **mode binaire écriture (`'wb'`)
        with open(filepath, 'wb') as f:
            #On écrit l’image morceau par morceau (par blocs de 1024 octets = 1 Ko)
            for chunk in response.iter_content(1024):
                f.write(chunk)
    else:
        print(f"Erreur de téléchargement pour l'image : {image_url}")