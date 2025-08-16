import os
import csv
import re
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


def etl_extract_page(pageurl):

    product_response = requests.get(pageurl)
    page_soup = BeautifulSoup(product_response.text, 'html.parser')
    #print(page_soup.prettify())
    book_info = {}
    product_page_url = pageurl
    #print(product_page_url)
    book_title = page_soup.title.string
    #print(book_title)
    univeral_product_code = page_soup.find("th", string="UPC").find_next_sibling("td").string
    #print(univeral_product_code)
    price_including_tax = page_soup.find("th", string= "Price (excl. tax)").find_next_sibling("td").string
    #print(price_including_tax)
    price_excluding_tax = page_soup.find("th", string = "Price (incl. tax)").find_next_sibling("td").string
    #print(price_excluding_tax)
    quantity_available = page_soup.find("th", string = "Availability").find_next_sibling("td").string
    #print(quantity_available)
    product_description = page_soup.find("div", attrs = {"id":"product_description"}).find_next_sibling("p").string
    #print(product_description)
    category = page_soup.find("a", string = "Books").find_next("a").string
    #print(category)
    """Review_rating below was a lucky call since I didn't 
    realize that a get('class') would return a list that
    is separated by a comma. I visualized it in the result
    dictionary and picked up on it"""
    review_rating = page_soup.find("p", class_=re.compile("star-rating")).get('class')[1]
    image_url_relative = page_soup.find("img").get('src')
    image_url = urljoin(pageurl, image_url_relative)
    book_info = {"product page url": product_page_url,
                  "book title": book_title,
                  "univeral product code": univeral_product_code,
                  "price including tax": price_including_tax,
                  "price excluding tax": price_excluding_tax,
                  "quantity available": quantity_available,
                  "product description": product_description,
                  "category": category,
                  "review rating": review_rating,
                  "image url": image_url}
    
    print(book_info)
    return book_info


def etl_parse_home(homeurl):
    home_page = requests.get(homeurl)
    home_soup = BeautifulSoup(home_page.text, 'html.parser')
    categories = home_soup.find("div", class_="side_categories").find_all("a")
    category_text = ""
    categories_url = ""
    category_info = {}
    for category in categories:
        abs_url = urljoin(homeurl, category.get('href'))

        """Below string.replace(" ","") wasn't working
        as I still got \n in the outputs. However string.strip()
        worked and gave the right output"""
        #category_text.append(category.string.strip())
        #categories_url.append(abs_url)
        category_info[category.string.strip()] = abs_url

    #print(category_info)
    return category_info
    


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

    #print(category_books_links)
    return category_books_links

def etl_load(load_data, output_file_path, field_name_header):

    #Since csv file already perform a newline by themselves hence we have to specify an empty newline here so it doesn't skip rows
    with open(output_file_path, mode = "w", newline="") as file_name:
        file_write = csv.DictWriter(file_name, delimiter=",", fieldnames= field_name_header)   
        file_write.writeheader()

        for data in load_data:
            file_write.writerow(data)    

def main():

    script_directory = os.path.dirname(os.path.abspath(__file__))
    home_url = input("Enter the homepage url you want to parse: ")
    response = requests.get(home_url, 'html.parser')
    if response.ok is True:
        category_info = etl_parse_home(home_url)
        for item in category_info:
            print(item)
    
    else:
        print("Either the website isn't responsive or you entered the wrong url.")
    
    type_category = input("Enter the category from the list you want to load(type 'all' for all): ")
    
    list_size = 0
    #print(len(category_info))
    while list_size <= len(category_info):
        if item!=type_category and list_size < len(category_info):
            list_size = list_size + 1

        elif item == type_category or type_category == "all":

            while True:
                for item in category_info:
                    category_url = category_info[item]
                    book_urls = etl_category_page(category_url)
                    for urls in book_urls:
                        book_info = etl_extract_page(urls)
                    load_path = os.path.join(script_directory, (f"{item}.csv"))
                    print()
                    break
                    #etl_load(load_data, load_path, )
                #print(f"I'll go ahead and parse {type_category}")
                #break

        elif item != type_category and list_size == len(category_info):
            print("Category Mismatch")
            break

        else:
            print("Unknown Error")
    
    
        
        
        
            


    

if __name__ == "__main__":
    main()
    


