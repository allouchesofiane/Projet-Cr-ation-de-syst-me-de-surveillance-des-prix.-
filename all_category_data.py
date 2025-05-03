import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os
import re
#url de l'index html
url = "https://books.toscrape.com/index.html"
# une fonction qui nous retour tous les liens de toutes les categories et le noms des categories
def all_category_data(url) :
    #la requete
    response = requests.get(url)
    #un objet soup pour recuperer les donnees en format text
    soup = BeautifulSoup(response.text, 'lxml')
    #une liste vide qui va recevoir tous les liens
    category_links = []
    #on cherche la balise a dans une ul 
    category_list = soup.find('ul', class_='nav nav-list').find('ul').find_all('a')
    #on boucle dans la liste des liens 
    for category in category_list:
        category_name = category.text.strip()
        #on joins la url et le href de la balise
        category_url = urljoin(url, category['href'])
        #on ajoute un tuple de (category_name, category_url) dans la listecategory_links = []
        category_links.append((category_name, category_url))
    #on retourne les liens de toutes les categories
    return category_links

#Récupère tous les liens des livres d'une catégorie (comme Phase 2)
def category_data(category_url) :
    book_links = []
    while category_url:
        #requete sur le code html du site
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'lxml')

        # Trouver tous les liens de livres sur cette page
        articles = soup.find_all('article', class_='product_pod')
        #boucler pour trouver les liens a avec l attribut href 
        for article in articles:
            a_tag = article.find('h3').find('a')
            relative_url = a_tag['href']
            #faire un lien complet absolue
            book_url = urljoin(category_url, relative_url)
            #ajouter les liens dans la liste book_links
            book_links.append(book_url)

        # Vérifier la pagination (bouton "next")
        next_button = soup.find('li', class_='next')
        if next_button:
            #trouver les liens a avec l attribut href 
            next_page = next_button.find('a')['href']
            #faire un lien complet absolue
            category_url = urljoin(category_url, next_page)
        else:
            category_url = None  
    #on retourne l'esemble des urls des livres de la gategory historical fiction
    return book_links

#  Fonction pour extraire les données d'un seul livre
def product_data(product_page_url) :
    #requette get pour recuperer le contenu de la page web et le stoquer dans la variable response 
    response = requests.get(product_page_url)
    print(response)
    if response.ok :
        soup = BeautifulSoup(response.text, 'lxml')
        #titre
        title = soup.find('h1').text
        #recuperer le code html de la table avec la classe 'table table-striped' 
        table = soup.find('table', class_ ='table table-striped')
        #recuperer tous les tr
        rows = table.find_all('tr')
        #boucle sur la table et les recuperer dans un dictionnaire 
        data = {row.th.text: row.td.text for row in rows}
    
        universal_product_code = data.get('UPC')
        price_including_tax = data.get('Price (incl. tax)')
        price_excluding_tax = data.get('Price (excl. tax)')
        number_available = data.get('Availability')
        #description
        description = soup.find('article', class_ = 'product_page')
        product_description = description.find_all('p')[3].text
        category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text
        #url image
        image_relative_url = soup.find('img')['src']
        image_url = urljoin(product_page_url, image_relative_url)
        #note
        # Note (étoiles)
        star_tag = soup.find('p', class_='star-rating')
        classes = star_tag.get('class')
        star_text = classes[1]
        stars_dict = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }
        review_rating = stars_dict.get(star_text, 0)
         
        # Téléchargement de l'image
        download_image(image_url, title, universal_product_code)

        #valeurs des headers
        data = [
            product_page_url, universal_product_code, title,
            price_including_tax, price_excluding_tax,
            number_available, product_description,
            category, review_rating, image_url
        ]
        return data
#Fonction pour télécharger l'image
def download_image(image_url, title, upc):
    # Créer le dossier 'images' s'il n'existe pas encore
    os.makedirs('images', exist_ok=True)
    
    # Nettoie le titre pour un nom de fichier valide
    valid_title = re.sub(r'[^A-Za-z0-9_]', '_', title).strip('_')
    
    # Limite le titre à 50 caractères max pour éviter des noms trop longs
    valid_title = valid_title[:50]
    
    # Prépare le nom du fichier image
    image_filename = os.path.join('images', f"{valid_title}_{upc}.jpg")
    
    # Télécharge l'image en petits morceaux (stream)
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(image_filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

#Sauvegarde dans un CSV    
def save_books_to_csv(books_data, category_name):

    # Nettoie le nom du fichier CSV pour éviter des caractères bizarres
    clean_category_name = re.sub(r'[^A-Za-z0-9_]', '_', category_name).strip('_')
    csv_file = f"{clean_category_name}.csv"
    #la liste des entetes
    headers = [
        'product_page_url', 'universal_product_code', 'title',
        'price_including_tax', 'price_excluding_tax',
        'number_available', 'product_description',
        'category', 'review_rating', 'image_url'
    ]
    with open(csv_file, 'w', encoding='utf-8') as file:
        #un objet qui nous permettera d ecrire dans fichier csv file
        writer = csv.writer(file)
        #on ecrit la premiere ligne (headers)
        writer.writerow(headers)
        #pour chaque livre on ecrit une ligne avec toutes les informations
        for book in books_data:
            writer.writerow(book)
#on retourne category_name, category_url dans une liste 
categories = all_category_data(url)

#on parcour chaque tuple dans categories             
for category_name, category_url in categories:
    #on recupere tous les liens des livres d'une categorie
    book_links = category_data(category_url)
    #on prepare une liste vide
    books_data = []
    #Pour chaque lien de livre
    for book_link in (book_links):
        #Cette fonction retourne les données du livre sous forme d’une liste (avec toutes les colonnes CSV)
        book_data = product_data(book_link)
        #ajoutes à la liste books_data
        if book_data:
            books_data.append(book_data)
    # Sauvegarder toutes les données dans un CSV avec la fonction save_books_to_csv 
    save_books_to_csv(books_data, category_name)