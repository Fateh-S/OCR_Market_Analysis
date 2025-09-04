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
