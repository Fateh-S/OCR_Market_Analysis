"""NOTICE: ALL THE COMMENTS WITH TRIPLE INVERTED COMMA's ARE
MEANT FOR ME AS GUIDANCE AND EVERY COMMENT WITH A # IS MEANT FOR
THE READER. """



import os
import csv
import re
import requests
from urllib.parse import urljoin

#This calls the module we have designed for extractions from the website
import extractions    
    
#Function that Creates and Loads data to CSV files    
def etl_load(load_data, output_file_path, field_name_header):

    #Since csv file already perform a newline by themselves hence we have to specify an empty newline here so it doesn't skip rows
    """If I turn the encoding to utf-16 and add a tab delimiter somehow the book titles disappear"""
    with open(output_file_path, mode = "w", newline="", encoding="utf-8-sig", errors="replace") as file_name:
        file_write = csv.writer(file_name)

        #Creating header for the CSV file   
        file_write.writerow(field_name_header)

        #for data in load_data:   
        file_write.writerows(load_data)    


#Function gets rid of symbols to correct file name
def safe_filename_os(filename: str) -> str:
    
    return re.sub(r'[<>:"/\\|?*]', "_", filename)      

def main():

    #Getting and storing the location of the script directory; adding an output folder to it.
    script_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Output_Data")
    os.makedirs(script_directory, exist_ok=True)

    #Adding a folder to the base. Organizational purposes.
    csv_folder = os.path.join(script_directory, "CSV_Files")
    os.makedirs(csv_folder, exist_ok= True)
    
    #choosing primary function to be executed.
    choose_option = input("Press '1' for csv file/s generation:\n"
                          "Press '2' to download image from book page:")
    
    
    if choose_option == "1":
        #Field Header is the book information, remains the same for all book. So we define it once.
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
        
        
        #Just a fancy prompt, it works for books to scrape only.
        home_url = input("Enter the homepage url you want to parse( press 1 to enter https://books.toscrape.com/index.html automatically): ")

        #Requesting a response from the website.
        if home_url == "1":
            home_url = "https://books.toscrape.com/index.html"
            response = requests.get(home_url, 'html.parser')
        
        else:
            print("Input missmatch. Either press 1 or paste the homeurl.The parser currently only supports Books to Scrape.")
            exit

        #Checking response from website.
        if response.ok is True:
            
            #Extracting and storing category url's against their name in a dictionary.
            category_info = extractions.extract_home(home_url)

            #Display all the type of categories
            for category_name in category_info.keys():
                print(category_name)

        
        else:
            print("Unable to get a postive response from the website.")


        #Choosing the category for data extractions and loading it into respective csv file/s.
        type_category = input("Enter the category from the list you want to load(type 'all' for all): ")
        
        #Storing the link to the input user provides.
        typed_cat_link = str(category_info.get(type_category, "")).strip()

        #Creating a list of category url's. Extracted from the category dictionary created earlier.
        category_links = list(category_info.values())


        if type_category == "all":
            # Process all categories
            for category_name, category_url in category_info.items():
                book_info = []  # reset for each category

                #Creating folders for each category. Organizing.
                category_folder = os.path.join (csv_folder, category_name)
                os.makedirs (category_folder, exist_ok= True)

                #Creating the CSV file per category in their respective folders.
                load_path = os.path.join(category_folder, f"{category_name}.csv")

                #Saving the list of book url's under each category. Considering pagination.
                book_urls = extractions.extract_category(category_url)

                #Extracting book information per links under each category.
                for url in book_urls:
                    book_info.append(extractions.extract_book(url))
                
                #Loading data to CSV
                etl_load(book_info, load_path, field_header)

                #Once done print informing successful creation of that category.
                print(f"CSV created for category {category_name}")

            #When all files are created.
            print("The file/s are created. Please check your CSV files.")



        #Check of link match for the typed category.
        elif typed_cat_link in category_links:
            # Process just one category
            book_info = []
            category_url = category_info[type_category]

            #Creating folder for the file.
            category_folder = os.path.join ( csv_folder, type_category)
            os.makedirs(category_folder, exist_ok= True)
            load_path = os.path.join(category_folder, f"{type_category}.csv")

            book_urls = extractions.extract_category(category_url)
            for url in book_urls:
                book_info.append(extractions.extract_book(url))

            etl_load(book_info, load_path, field_header)
            print(f"CSV created for category {type_category}. Please check the file.")

        else:
            print("Category Mismatch. Either category doesn't exist or you mis-spelled it.")





    #Choosing option for the main operation type.
    elif choose_option == "2":

        book_page_url = input("Enter the url of the book page to download it's image: ")
        book_page_response = requests.get(book_page_url)


        if book_page_response.status_code == 200:
            book_info = extractions.extract_book(book_page_url)

            #Getting the image url and book name from the book information list created.
            book_image_url = book_info[-1]
            book_name = str(book_info[1])

            #Removing symbols from name if any.
            book_name = safe_filename_os(book_name).strip()
            
            #Directing the location of download
            images_folder = os.path.join(script_directory, "Images")
            os.makedirs(images_folder, exist_ok= True)
            book_image_folder = os.path.join(images_folder, book_name)
            os.makedirs(book_image_folder, exist_ok= True)

            extractions.image_extract_save(book_image_url, book_image_folder, book_name)

        else:
            print("Unable to get a positive response from the url.")




    else:
        #Restart the program
        print("Input should be either '1' or '2'. Try again.")
        main()

        
    
if __name__ == "__main__":
    main()
    


