#!/usr/bin/python3
#
# Usage: scrape-all.py FILE
# Scrapes all sites listed in FILE and prints the execution
# time. In Linux use ctrl+z to stop execution.

import sys
import os
import re
import time

def main():
  with open(sys.argv[1]) as file:
    lines = file.readlines()
  startTime = time.time()
  for line in lines:
    command = "python betbrain.py " + line.rstrip()
    print(command)
    os.system(command)
  print("==================================")
  print("--- %s seconds ---" % (time.time() - startTime))

if __name__ == '__main__':
  main()
