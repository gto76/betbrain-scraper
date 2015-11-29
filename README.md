Odds Scraper
============

Python scripts for scraping odds from betting websites.
Runs on Python3 and needs BeautifulSoup4 library.

How to run on…
--------------

### Windows
```
>pip install BeautifulSoup4
>py betbrain.py [URL/FILE]
```
In order for pip to work, python's Scripts dir needs to be in PATH.

### UNIX
```
$ sudo apt-get install python3-bs4
$ ./betbrain.py [URL/FILE]
```

Benchmarks
----------

### v6
```
python3 scrape-all.py test-urls.txt
--- 204.26561331748962 seconds ---
```

