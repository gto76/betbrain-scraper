#!/usr/bin/python3
#
# Usage: paralel-scrape.py URLS-FILE [OUTPUT-DIR] [NUM-OF-SUBPROCESSES]
# Scrapes all sites listed in URLS-FILE and saves results in
# OUTPUT-DIR. At the end it prints the execution time.

import sys
import os
import re
import time
import subprocess
from datetime import datetime

DEFAULT_OUTPUT_DIR = "results"
DEFAULT_CHUNK_SIZE = 8

def main():
  startTime = time.time()
  start(sys.argv)
  print("==================================")
  print("--- %s seconds ---" % (time.time() - startTime))

def start(argv):
  interpreter = getInterpreter()
  urls = getUrls(argv)
  outputDir = getOutputDir(argv)
  chunkSize = getChunkSize(argv)
  for chunk in splitList(urls, chunkSize):
    batchProcess(chunk, interpreter, outputDir)

# Retruns right name of an interpreter.
def getInterpreter():
  if os.name == "posix":
    return "python3"
  else:
    return "python"

def getUrls(argv):
  with open(argv[1]) as file:
    return file.readlines()

def getOutputDir(argv):
  if len(argv) <= 2:
    return DEFAULT_OUTPUT_DIR
  else:
    return sys.argv[2]

def getChunkSize(argv):
  if len(argv) <= 3:
    return DEFAULT_CHUNK_SIZE
  else:
    return int(sys.argv[3])

# Yields successive n-sized chunks from list.
def splitList(list, chunkLength):
  for i in range(0, len(list), chunkLength):
    yield list[i:i+chunkLength]

# Paralelly scrapes urls that are contained in chunk
def batchProcess(chunk, interpreter, outputDir):
  subprocesses = []
  for url in chunk:
    url = url.rstrip()
    filename = getFilename(url, outputDir)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    command = [ interpreter, "betbrain.py", url, filename]
    print(' '.join(command))
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocesses.append(process)
  for p in subprocesses:
    out, err = p.communicate()
    if err:
      print(err.decode('unicode_escape'))
    # EX: printOut(out)

def getFilename(url, outputDir):
  time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
  game = re.sub('^.*\.com/', '', url)
  game = re.sub('/$', '', game)
  game = re.sub('/', '_', game)
  return outputDir+"/"+game+"_"+time+".txt"

# def printOut(out):
#   string = out.decode('unicode_escape')
#   head = string.splitlines()[1:10]
#   print('\n'.join(head))

if __name__ == '__main__':
  main()

