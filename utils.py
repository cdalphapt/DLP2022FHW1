import os
import PyPDF2


class pdfPaper:
    #The class contains basic info about the paper. (e.g title, ref, etc.)
    def __init__(self, dir):
        self.dir = dir
        pdfReader = PyPDF2.PdfFileReader(open(dir, 'rb'))
        self.title = pdfReader.getDocumentInfo().title
        #print(self.name)
    pass
