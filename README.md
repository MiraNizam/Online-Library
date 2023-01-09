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

You need to run the script from the Online-Library/ folder
The default values are in the range 1 to 10 of the book.
```
python3 main.py
```
To download another list of books, you must specify the range:

```
python3 main.py --start_id=11 --end_id=15
```


### Project Goals
This code was written for educational purposes as part of an online course for web developers at dvmn.org.




