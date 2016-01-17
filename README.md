Betbrain Scraper
================

Python scripts for scraping odds from betting websites.
Runs on Python3 and needs BeautifulSoup4 library.

How to run on…
--------------

### Windows
```
>pip install BeautifulSoup4
>py betbrain.py
```
In order for pip to work, python's Scripts dir needs to be in PATH.

### UNIX
```
$ sudo apt-get install python3-bs4
$ ./betbrain.py
```

Scripts
-------
### betbrain.py

`Usage: betbrain.py [URL or FILE] [OUTPUT-FILE]`  

Scrapes odds from passed betbrain page and writes them to stdout, or file if specified.

### paralel-scrape.py

`Usage: paralel-scrape.py URLS-FILE [OUTPUT-DIR] [NUM-OF-SUBPROCESSES]` 

Scrapes all sites listed in URLS-FILE and saves results in OUTPUT-DIR. At the end it prints the execution time.
