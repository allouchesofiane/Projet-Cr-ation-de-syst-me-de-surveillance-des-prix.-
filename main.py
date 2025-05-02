#import du module requests et beautifulsoup

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin  
import csv
#declaration et affectation de la variable URL 
product_page_url = "https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"

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
    #fichier csv
    csv_file = 'product_data.csv'
    #la liste des entetes
    headers = [
        'product_page_url', 'universal_product_code', 'title',
        'price_including_tax', 'price_excluding_tax',
        'number_available', 'product_description',
        'category', 'review_rating', 'image_url'
    ]
    #valeurs des headers
    data = [
        product_page_url, universal_product_code, title,
        price_including_tax, price_excluding_tax,
        number_available, product_description,
        category, review_rating, image_url
    ]
    #ecrire les donnees dans un fichier csv
    with open(csv_file, 'w', encoding='UTF8') as file :
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerow(data)

    print(product_page_url)
    print(universal_product_code)
    print(title)
    print(price_including_tax)
    print(price_excluding_tax)
    print(number_available)
    print(product_description)
    print(category)
    print(image_url)
    print(review_rating)


 