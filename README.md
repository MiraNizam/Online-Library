# Book parser from tululu.org

The script that help you to download books and information about them posted on the site [tululu.org](tululu.org).
With this script, you can get the following information:

* Title of the book
* book author
* Comments
* Genre
* Book cover
* Book in .txt format

## Getting Started

Below you will find instructions on how to use **Book parser tululu.org**.  

### Prerequisites

Please be sure that **Python3** is already installed. 

### Installing
1. Clone the repository:
```
git clone https://github.com/MiraNizam/Online-Library.git
```
2. Create a new virtual environment env in the directory
```
python -m virtualenv env
```
3. Activate the new environment
```
source env/bin/activate
``` 
4. Use pip (or pip3, if there is a conflict with Python2) to install dependencies in new environment:
```
pip install -r requirements.txt
```

### How to run code:
You can parse: range of books, pages or full category.

You need to run the script from the Online-Library/ folder

Script has command-line interface for comfortable using. 
Interface includes the following commands: 

for ```main.py```: 

* ```--start_id``` the start position in range for parsing, default: 1
* ```--end_id``` the end position in range for parsing, default: 10

for ```parse_tululu_category.py```:

* ```--start_page```  the start position in range for parsing, default: 1 
* ```--end_page``` the end position in range for parsing, default: the last page in category
* ```--dest_folder``` path to the catalogue with parse result: images and books,  as default: folders named images and books
* ```--skip_imgs``` Don't download images, change to True. Default: False. 
* ```--skip_txt```Don't download txt, change to True. Default: False. 
* ```--json_path``` path to *.json file. Default current folder. 
* ```--help``` use it if you forget the information above

Examples: 

Parse book in range from 1 to 10
```
python main.py
```
Parse book in range from 11 to 15
```
python main.py --start_id=11 --end_id=15
```
Parse full category
```
python parse_tululu_category.py
```
Parse page **600**, save images and books in folder **page_600**, save .json file in folder **json_file** and skip images
```
python parse_tululu_category.py --start_page 600 --end_page 601 --dest_folder page_600 --json_path json_file --skip_imgs True
```


### Project Goals
This code was written for educational purposes as part of an online course for web developers at [dvmn.org](https://dvmn.org/).




