
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin  
import csv



#recuperer les donnes de toute une category de livres.
#url de la categorie historical fiction
category_url = 'https://books.toscrape.com/catalogue/category/books/historical-fiction_4/page-1.html'

# une fonction qui va retourner l'ensemble des liens,compris ceux de la pagination
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
        #valeurs des headers
        data = [
            product_page_url, universal_product_code, title,
            price_including_tax, price_excluding_tax,
            number_available, product_description,
            category, review_rating, image_url
        ]
        return data
#  Fonction pour sauvegarder les données dans un CSV
def save_books_to_csv(books_data, category_name):

    csv_file = f"{category_name}.csv"
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

# récupérer le nom de la catégorie pour l’utiliser comme nom de fichier CSV.
category_name = category_url.strip('/').split('/')[-2]

# Récupérer tous les liens des livres de la catégorie
book_links = category_data(category_url)

# On prépare une liste vide qui va recevoir les données de tous les livres.
all_books_data = []
for book_link in book_links :
    book_data = product_data(book_link)
    if book_data:
        all_books_data.append(book_data)

# Sauvegarder toutes les données dans un CSV avec la fonction save_books_to_csv 
save_books_to_csv(all_books_data, category_name)