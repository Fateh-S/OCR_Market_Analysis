import os
import csv
import re
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


def extract_book(pageurl):

    product_response = requests.get(pageurl)
    page_soup = BeautifulSoup(product_response.text, 'html.parser')
    #print(page_soup.prettify())
    book_info = []
    product_page_url = pageurl
    #print(product_page_url)
    book_title = page_soup.title.string
    #print(book_title)
    univeral_product_code = page_soup.find("th", string="UPC").find_next_sibling("td").string
    #print(univeral_product_code)
    price_including_tax = page_soup.find("th", string= "Price (excl. tax)").find_next_sibling("td").string.replace("Â", "")
    #print(price_including_tax)
    price_excluding_tax = page_soup.find("th", string = "Price (incl. tax)").find_next_sibling("td").string.replace("Â", "")
    #print(price_excluding_tax)
    quantity_available = page_soup.find("th", string = "Availability").find_next_sibling("td").string
    #print(quantity_available)
    product_description = page_soup.find("div", attrs = {"id":"product_description"})
    """Found an error here where a product didn't have a description,
    figured my best bet before I run all is to run books, since 
    that category had all the books in it. Ran successfully after this change"""
    if product_description:
        product_description = product_description.find_next_sibling("p").string.replace("â","'")
    else:
        product_description = "No Description"
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
    book_info = [product_page_url,
                book_title,
                univeral_product_code,
                price_including_tax,
                price_excluding_tax,
                quantity_available,
                product_description,
                category,
                review_rating,
                image_url]
    
    #print(book_info)
    return book_info


def extract_home(homeurl):
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
    


def extract_category(cateurl):

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
"""The system was giving me an etl_load error and it turns out it was because I had
the csv file open and was trying to write it at the same time. Just read the error 
it was a permission error, getting to know how to read errors"""
def etl_load(load_data, output_file_path, field_name_header):

    #Since csv file already perform a newline by themselves hence we have to specify an empty newline here so it doesn't skip rows
    """If I turn the encoding to utf-16 and add a tab delimiter somehow the book titles disappear"""
    with open(output_file_path, mode = "w", newline="", encoding="utf-8-sig", errors="replace") as file_name:
        file_write = csv.writer(file_name)   
        file_write.writerow(field_name_header)

        #for data in load_data:
            
        file_write.writerows(load_data)    

  
def main():

    field_header = ["Product Page URL",
                    "Book Title",
                    "Universal Product Code",
                    "Price Including Tax",
                    "Price Excluding Tax",
                    "Quantity Available",
                    "Product Description",
                    "Category",
                    "Review Rating",
                    "Image URL"]
    script_directory = os.path.dirname(os.path.abspath(__file__))
    home_url = input("Enter the homepage url you want to parse( press 1 to enter https://books.toscrape.com/index.html automatically): ")
    if home_url == "1":
        home_url = "https://books.toscrape.com/index.html"
        
    response = requests.get(home_url, 'html.parser')
    if response.ok is True:
        category_info = extract_home(home_url)
        for item in category_info.keys():
            print(item)

            #print(category_info.keys())
        #item = str(item).strip()
    
    else:
        print("Either the website isn't responsive or you entered the wrong url.")
    
    type_category = input("Enter the category from the list you want to load(type 'all' for all): ")
    
    """book_info = []
    list_size = 0
    typed_cat_link = str(category_info[type_category]).strip()
    category_links = []
    #print(len(category_info))
    for value in category_info.values():
        category_links.append(value)
    
    
    while list_size < len(category_info):
        if typed_cat_link != category_links[list_size]:
                list_size = list_size + 1
                continue
        #print(category_info[type_category])
        if typed_cat_link == str(category_links[list_size]).strip() or type_category == "all":


            
            

            
            for item in category_info:
                load_path = os.path.join(script_directory, (f"{item}.csv"))
                category_url = category_info[item]
                book_urls = extract_category(category_url)
                for urls in book_urls:
                    book_info.append(extract_book(urls))
  
                    
                if type_category == "all":
                    initiate_csv = etl_load(book_info, load_path, field_header)
                    print("The file/s is/are created.")

                else:
                    initiate_csv = etl_load(book_info, load_path, field_header) 
                    print("Please make sure your csv file has no issues.")
                    break
            
                    #etl_load(load_data, load_path, )
                    
            print(f"Please check for csv file for the category {type_category}")
                

        elif typed_cat_link != category_links[list_size] and list_size < len(category_info):
            print("Category Mismatch")
            break

        else:
            print("Category Mismatch")
            break"""
    
    book_info = []
    typed_cat_link = str(category_info.get(type_category, "")).strip()
    category_links = list(category_info.values())

    if type_category == "all":
        # Process all categories
        for item, category_url in category_info.items():
            book_info = []  # reset for each category
            load_path = os.path.join(script_directory, f"{item}.csv")

            book_urls = extract_category(category_url)
            for url in book_urls:
                book_info.append(extract_book(url))

            etl_load(book_info, load_path, field_header)
            print(f"CSV created for category {item}")

        print("The file/s are created. Please check your CSV files.")

    elif typed_cat_link in category_links:
        # Process just one category
        book_info = []
        category_url = category_info[type_category]
        load_path = os.path.join(script_directory, f"{type_category}.csv")

        book_urls = extract_category(category_url)
        for url in book_urls:
            book_info.append(extract_book(url))

        etl_load(book_info, load_path, field_header)
        print(f"CSV created for category {type_category}. Please check the file.")

    else:
        print("Category Mismatch")

        
    
    
        
        
        
            


    

if __name__ == "__main__":
    main()
    


