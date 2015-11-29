#!/usr/bin/python3
#
# Usage: trylly-paralel-scrape.py FILE NUM-OF-SUBPROCESSES
# Scrapes all sites listed in FILE and prints the execution
# time. In Linux use ctrl+z to stop execution.

import sys
import os
import re
import time
import subprocess

def main():
  startTime = time.time()
  with open(sys.argv[1]) as file:
    lines = file.readlines()

  files = lines
  processes = set()
  max_processes = int(sys.argv[2])

  for name in files:
    name = name.rstrip()
    command = "python3 betbrain.py "+name+" | head" 
    processes.add(subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
    # processes.add(subprocess.Popen(command, shell=True))
    if len(processes) >= max_processes:
      os.wait()
      processes.difference_update([p for p in processes if p.poll() is not None])  

  print("==================================")
  print("--- %s seconds ---" % (time.time() - startTime))

if __name__ == '__main__':
  main()


