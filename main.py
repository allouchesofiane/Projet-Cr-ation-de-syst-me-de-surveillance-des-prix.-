# --- main.py ---
from functions import (
    fetch_page, parse_product_data, get_review_rating,
    save_to_csv, get_all_categories, get_all_book_links, download_image
)

url = "https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"

def scrape_product(url):
    """Scrape un produit spécifique et sauvegarde dans product_data.csv."""
    soup = fetch_page(url)
    if soup:
        data = parse_product_data(soup, url)
        data['review_rating'] = get_review_rating(soup)
        save_to_csv(data, 'product_data.csv')
    else:
        print("Erreur lors du scraping du produit.")
scrape_product(url)


category_url = 'https://books.toscrape.com/catalogue/category/books/historical-fiction_4/page-1.html'


def scrape_category(category_url):
    """Scrape tous les livres d'une catégorie et sauvegarde dans un CSV."""
    book_links = get_all_book_links(category_url)
    all_books_data = []
    for book_url in book_links:
        soup = fetch_page(book_url)
        if soup:
            data = parse_product_data(soup, book_url)
            data['review_rating'] = get_review_rating(soup)
            all_books_data.append(data)
            download_image(data['image_url'])
    # Création du nom de fichier CSV
    category_name = category_url.strip('/').split('/')[-2].replace('-', '_')
    csv_filename = f"{category_name}.csv"
    #On enregistre la liste complète dans un fichier CSV, une ligne par livre
    save_to_csv(all_books_data, csv_filename)
scrape_category(category_url)


def scrape_all_categories():
    """Scrape toutes les catégories et sauvegarde chaque résultat dans un CSV."""
    categories = get_all_categories()
    #on boucles sur chaque paire (nom de catégorie, URL) du dictionnaire
    for name, url in categories.items():
        scrape_category(url)
scrape_all_categories()

  