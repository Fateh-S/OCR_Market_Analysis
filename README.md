<H1 align="center"> OCR Market Analysis</H1>

### About
*Book information tracking from [Books to Scrape](https://books.toscrape.com/index.html). Currently an extract and load pipline only. With CSV file generator, folder organizer and image downloader.*


<p align="center">
  <img src="https://png.pngtree.com/png-clipart/20220107/ourmid/pngtree-book-png-image_4224464.png
  " alt="Book Scraping" width="200"/>
</p>

---


## ✨ Features 


A textual terminal feed that requests for instructions on which it performs the following for the website (Books to Scrape):

> ### Pagination (Extraction)
>> The Script makes sure to cover extractions of book data regardless of the number of pages. It will loop through them all regardless of the number of pages.
---
> ###  Extract
>     📝 Book Details
>> This includes all the necessary information regarding the meta data of the book. Includes the following information:
>> 1. The absolute page url of the book.
>> 2. Book Title
>> 3. Universal Product Code
>> 4. Price (Including Tax)
>> 5. Price (Excluding Tax)
>> 6. Quantity Available
>> 7. Product Description
>> 8. Category 
>> 9. Review Rating
>> 10. Absolute Image URL
>
>     📚 Extracting list of Books in categories
>> For any and all categories, listing down the links to the books that exist inside them.
>
>     🏷️ Extracting each category name alongside their absolute URLs
>> From the Books to Scrape homepage, parsing through all the categories and returning their name alongside their absolute URLs.
---
> ### 💾 Load
>> - Save data into UTF-8 CSVs (Excel-friendly, no weird encoding issues).
>> - Neat and organized data managed under their respective fieldnames.
---
> ### Safe-Naming (Windows) 
>> - Will make sure file name fall under OS naming standards and omits any special characters that aren't allowed.
---
> ### 📂 Smart Folder Hierarchy
>> - Images and CSVs go into an organzied forlder structure
>>  ```Organization
>> Output_Data/
>> ├── CSV_Files/
>> │   ├── Travel/
>> │   │   └── Travel.csv
>> │   ├── Mystery/
>> │   │   └── Mystery.csv
>> │   └── ...
>> └── Images/
>>     ├── Book_Name_1/
>>     │   └── Book_Name_1.png
>>     └── Book_Name_2/
>>         └── Book_Name_2.png


` Notice: The Output Data Folder is created under the same folder structure that your script resides in. `
---
---

## ⚙️ Installation

Clone the [repository](https://github.com/Fateh-S/OCR_Market_Analysis/tree/dev) to the folder of your liking. It is preferred to create a Python Virtual Environment with the following dependencies for the Script to run properly. Make sure extractions.py and OCR_Market_Analysis_Fateh_Shehryar.py sit in the same folder.

### Dependencies
- requests
- bs4
- extractions (requires to be in the same folder as OCR_Market_Analysis_Fateh_Shehryar.py)
- csv (built-in)
- re (built-in)
- os (built-in)
- urllib (built-in)
---
---

## Usage

### On Windows (Bash)

1.  Traverse to the installed folder: 

> $ cd Parent_Folders/Installed_Folder

2. Create a Virtual Environment:

> $ pyton -m venv venv

3. Activate te Virtual Environment:

> source venv/Scripts/activate

4. Install the required libraries:

> pip install -r requirements.txt

OR explicitly install the following libraries:

> requests<br>
> bs4

5. Run the Script (Bash):
>
>> $ python OCR_Market_Analysis_Fateh_Shehryar.py<br>
>
> You will be prompted with the options to choose between the operations:
>>---
>> CSV file/s generation (Press 1)<br>
>>> A prompt will then be generated asking you to choose between creating all CSV file or to create just for te typed one: <br>
>>>
>>> Type 'all'
>>>> 1. This will create all the CSV for each category and store them in their respective categories.
>>>>
>>>> 2. Prompt user to check files once done.
>>> 
>>> Type 'Category Name'
>>>> 1. Creates CSV for that respective category in it's respective folder. <br>
>>>>
>>>> 2. Prompts user to check file once done.
>> ---
>>
>> Image Downloader (Press 2) <br>
>>> The system will ask for the URL for the bookpage that requires the extraction of it's image.
>>>> 1. Save the image of the Book Name in it's respective folder with the Book Name.
>>>>
>>>> 2. File is currently being saved as a png.
>>>>
>>>> 3. Prompts user to check files.

---
---

## 🛡 Notes and Caveats

 * Functions only with Books To Scrape's [website](https://books.toscrape.com/index.html).

 * If you use Excel, make sure to open CSVs with UTF-8 encoding (they’re saved as utf-8-sig).

 * Transforming data isn't yet added to the Script.
---
---

## 🌟 Future Additions

* Adding data transformation 
* Adding features for data visualization
* Generalize to scrape other e-commerce websites

---
---

## 📜 Licence

MIT License © 2025 Fateh Shehryar
---
---




