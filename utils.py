import os
import PyPDF2
import string
import re


class pdfPaper:
    #The class contains basic info about the paper. (e.g title, ref, etc.)
    def __init__(self, dir):
        self.dir = dir
        pdfReader = PyPDF2.PdfFileReader(open(dir, 'rb'))
        self.title = pdfReader.getDocumentInfo().title
        self.contentTxt = ""
        self.refs = []
        for page in pdfReader.pages:
            self.contentTxt += page.extract_text()
        print(self.contentTxt)

    def FindRefs(self):
        tempLowercTxt = self.contentTxt.lower()
        tempRefStartContainer = [_.start() for _ in re.finditer('references', tempLowercTxt)]
        print()
        print(self.contentTxt[tempRefStartContainer[-1]::1])
        #for page in pdfReader.getFields()
        #self.refs = []

        #print(self.name)
    pass
