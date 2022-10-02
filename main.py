from getopt import getopt
import utils
import urllib.request
import re
import os
import sys

debug = 0
opts, args =  getopt(sys.argv[1:], 'd')
for op, value in opts:
    if op == "-d":
        debug = 1;

if __name__ == '__main__':
    originPaper = utils.pdfPaper('./1904.05939.pdf')
    originPaper.FindRefs()
    originPaper.ShowRefs()
    originPaper.DownloadAllPapers()



