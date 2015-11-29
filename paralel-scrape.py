#!/usr/bin/python3
#
# Usage: paralel-scrape.py FILE NUM-OF-SUBPROCESSES
# Scrapes all sites listed in FILE and prints the execution
# time. In Linux use ctrl+z to stop execution.

import sys
import os
import re
import time
import subprocess

def main():
  interpreter = getInterpreter()
  startTime = time.time()
  with open(sys.argv[1]) as file:
    lines = file.readlines()
  for chunk in splitList(lines, int(sys.argv[2])):
    batchProcess(chunk, interpreter)
  print("==================================")
  print("--- %s seconds ---" % (time.time() - startTime))

# Retruns right name of an interpreter.
def getInterpreter():
  if os.name == "posix":
    return "python3"
  else:
    return "python"

# Yields successive n-sized chunks from list.
def splitList(list, chunkLength):
  for i in range(0, len(list), chunkLength):
    yield list[i:i+chunkLength]

# Paralelly scrapes urls that are contained in chunk
def batchProcess(chunk, interpreter):
  subprocesses = []
  for line in chunk:
    command = interpreter+" betbrain.py "+line.rstrip()+" | head"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocesses.append(process)
  for p in subprocesses:
    out, err = p.communicate()
    print(out.decode('unicode_escape'))

    # output = subprocess.getoutput(command)
    # print(output)

if __name__ == '__main__':
  main()

