# --- main.py ---
from functions import (
   scrape_product, scrape_category, scrape_all_categories
)

url = "https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"
scrape_product(url)

category_url = 'https://books.toscrape.com/catalogue/category/books/historical-fiction_4/page-1.html'
scrape_category(category_url)

scrape_all_categories()

  