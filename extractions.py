"""NOTICE: ALL THE COMMENTS WITH TRIPLE INVERTED COMMAS ARE FOR SELF REVIEW, 
COMMENTS WITH A # ARE MEANT FOR THE READER."""

#This module consists of all the extraction functions for the Market Analysis Project.


import os
import re
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin



#Take in a url to extract the book information for that page.
def extract_book(pageurl):


    product_response = requests.get(pageurl)

    #In main this was done using response.ok, performs the same.
    if product_response.status_code == 200:
        page_soup = BeautifulSoup(product_response.text, 'html.parser')
        
        #Create an empty list to recieve book data.
        book_info = []

        #Extracting all the book metadata.
        book_title = page_soup.title.string
        univeral_product_code = page_soup.find("th", string="UPC").find_next_sibling("td").string
        price_including_tax = page_soup.find("th", string= "Price (excl. tax)").find_next_sibling("td").string.replace("Â", "")
        price_excluding_tax = page_soup.find("th", string = "Price (incl. tax)").find_next_sibling("td").string.replace("Â", "")
        quantity_available = page_soup.find("th", string = "Availability").find_next_sibling("td").string
        product_description = page_soup.find("div", attrs = {"id":"product_description"})


        """Found an error here where a product didn't have a description,
        figured my best bet before I run all is to run books, since 
        that category had all the books in it. Ran successfully after this change"""
        if product_description:
            product_description = product_description.find_next_sibling("p").string.replace("â","'")
        else:
            product_description = "No Description"


        category = page_soup.find("a", string = "Books").find_next("a").string

        """Review_rating below was a lucky call since I didn't 
        realize that a get('class') would return a list that
        is separated by a comma. I visualized it in the result
        dictionary and picked up on it"""
        review_rating = page_soup.find("p", class_=re.compile("star-rating")).get('class')[1]
        image_url_relative = page_soup.find("img").get('src')
        image_url = urljoin(pageurl, image_url_relative)


        #Inserting the book metadata into a list.
        book_info = [pageurl,
                    book_title,
                    univeral_product_code,
                    price_including_tax,
                    price_excluding_tax,
                    quantity_available,
                    product_description,
                    category,
                    review_rating,
                    image_url]
        
        return book_info
    
    else:
        print("Unable to get a positive response from the url.")
        exit

#Take in category url and print a list of all the books under it. Considers pagination.
def extract_category(cateurl):

    #Check for response from url.
    category_response = requests.get(cateurl)
    if category_response.status_code == 200:
        category_soup = BeautifulSoup(category_response.text, 'html.parser')

        #URL will be later used to get the absolute url book urls and to move to next page.
        new_url = cateurl

        #Create a list to store all the URLs under that category.
        category_books_links = []

        #Will run for (at least one) all the pages until there isn't a next found to move page.
        while True:
            books_in_category = category_soup.find_all("div", class_="image_container")
            
            for book in books_in_category:

                #Getting and storing absolute url for each book.
                book_url = urljoin(new_url, (book.find("a").get('href')))
                category_books_links.append(book_url)
            
            #If condition to exit loop.
            if len(category_soup.find_all("li", class_="next")) == 0:
                break

            #Changing URL to move to the next page.
            pagination = category_soup.find("li", class_="next").find("a").get('href')
            new_url = urljoin(new_url, pagination)

            new_url_response = requests.get(new_url)
            if new_url_response.status_code == 200:
                category_soup = BeautifulSoup(new_url_response.text, 'html.parser')

            else:
                print(f"{new_url} did not give a positive response.")
                exit

        return category_books_links
    
    else:
        print("The categories page did not give a positive response.")
        exit

    """The system was giving me an etl_load error and it turns out it was because I had
    the csv file open and was trying to write it at the same time. Just read the error 
    it was a permission error, getting to know how to read errors"""

#Take in a homepage url and return a dictionary with key being the name and value being the urls of categories.
def extract_home(homeurl):

    home_page = requests.get(homeurl)

    #Checking for positive response from homepage.
    if home_page.status_code == 200:
        home_soup = BeautifulSoup(home_page.text, 'html.parser')
        categories = home_soup.find("div", class_="side_categories").find_all("a")
        category_info = {}

        for category in categories:

            #Getting absolute url for each category
            abs_url = urljoin(homeurl, category.get('href'))

            """Below string.replace(" ","") wasn't working
            as I still got \n in the outputs. However string.strip()
            worked and gave the right output"""
            #Removing whitespace for the keys and assigning them urls.
            category_info[category.string.strip()] = abs_url

        return category_info
    

    else:
        print("Difficulty getting response from the homepage.")
        exit


def image_extract_save(image_url, relative_download_dir, book_name):

    #Setting image compression (png)
    book_name = book_name + ".png"

    #Checking for response from image url
    response = requests.get(image_url)
    if response.status_code == 200:

        #Creating a png file in the respective folder.
        abs_image_path = os.path.join(relative_download_dir, book_name)
        with open(abs_image_path, "wb") as image_file:
            for chunk in response.iter_content(256):
                image_file.write(chunk)
        
        print(f"Look for the downloaded file in: {abs_image_path}" )

    else:
        print("Unable to get a positive response from url, image not downloaded.")
        exit


"""This is something I'm not aware of and asked chatgpt to do it for me instead
what I don't understand in here is str -> str"""