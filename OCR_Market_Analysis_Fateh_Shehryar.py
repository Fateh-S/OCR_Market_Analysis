import pandas
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


def etl_extract_page(pageurl):

    product_response = requests.get(pageurl)
    page_soup = BeautifulSoup(product_response.text, 'html.parser')
    #print(page_soup.prettify())
    product_page_url = pageurl
    print(product_page_url)
    book_title = page_soup.title.string
    print(book_title)
    univeral_product_code = page_soup.find("th", string="UPC").find_next_sibling("td").string
    print(univeral_product_code)
    price_including_tax = page_soup.find("th", string= "Price (excl. tax)").find_next_sibling("td").string
    print(price_including_tax)
    price_excluding_tax = page_soup.find("th", string = "Price (incl. tax)").find_next_sibling("td").string
    print(price_excluding_tax)
    quantity_available = page_soup.find("th", string = "Availability").find_next_sibling("td").string
    print(quantity_available)
    product_description = page_soup.find("div", attrs = {"id":"product_description"}).find_next_sibling("p").string
    print(product_description)
    category = page_soup.find("a", string = "Books").find_next("a").string
    print(category)
    #review_rating = page_soup

def etl_parse_home(homeurl):
    home_page = requests.get(homeurl)
    home_soup = BeautifulSoup(home_page.text, 'html.parser')
    categories = home_soup.find("div", class_="side_categories").find_all("a")
    categories_url = []
    category_text = []
    for category in categories:
        abs_url = urljoin(homeurl, category.get('href'))

        """Below string.replace(" ","") wasn't working
        as I still got \n in the outputs. However string.strip()
        worked and gave the right output"""
        category_text.append(category.string.strip())
        categories_url.append(abs_url)

    print(categories_url)
    print(category_text)
    


def etl_category_page(cateurl):

    category_response = requests.get(cateurl)
    category_soup = BeautifulSoup(category_response.text, 'html.parser')
    new_url = cateurl
    category_books_links = []

    while True:
        books_in_category = category_soup.find_all("div", class_="image_container")
        
        for book in books_in_category:
            book_url = urljoin(new_url, (book.find("a").get('href')))
            category_books_links.append(book_url)
        
        if len(category_soup.find_all("li", class_="next")) == 0:
            break
        pagination = category_soup.find("li", class_="next").find("a").get('href')
        new_url = urljoin(new_url, pagination)
        category_soup = BeautifulSoup(requests.get(new_url).text, 'html.parser')

    print(category_books_links)

        

def main():
    etl_parse_home("https://books.toscrape.com/index.html")

if __name__ == "__main__":
    main()
    




