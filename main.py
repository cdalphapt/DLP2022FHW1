import utils
import urllib.request
import re
import os

if __name__ == '__main__':
    originPaper = utils.pdfPaper('./2207.06103v2.pdf')
    originPaper.FindRefs()



