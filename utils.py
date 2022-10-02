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
        tempRefContainer = [subStr.start() for subStr in re.finditer('references', tempLowercTxt)]
        tempAllRefs = self.contentTxt[tempRefContainer[-1]::1]#Find last "references"
        tempAllRefs = FormatCorrection(tempAllRefs)
        tempRefContainer = [subStr.start() for subStr in re.finditer('\[[0-9]+\]', tempAllRefs)]
        for i in range(len(tempRefContainer)):
            if i == len(tempRefContainer) - 1:
                tempRef = tempAllRefs[tempRefContainer[i]+2+len(str(i))::1]
                tempRef = tempRef.strip()
                self.refs.append(tempRef)
            else:
                tempRef = tempAllRefs[tempRefContainer[i]+2+len(str(i)):tempRefContainer[i+1]:1]
                tempRef = tempRef.strip()
                self.refs.append(tempRef)
        for ref in self.refs:
            print('--------------------------------------------------------------------------')
            print(ref)

            



        #req = urllib.request.Request('https://dblp.uni-trier.de/search//publ/inc?q=Offline%20Reinforcement%20Learning&s=ydvspc&h=30&b='+str(j))
        #response = urllib.request.urlopen(req)
        #the_page = response.read().decode('utf-8')

def FormatCorrection(oriStr):
    #correct the format for later process
    tempPosList = [subStr.start() for subStr in re.finditer(r'-\n[a-z]', oriStr)]
    #Clear hyphen, but keep en-dash unchanged (hpoefully)
    #print(connectPosList)
    tempPosList = tempPosList[-1::-1]
    for subStrIndex in tempPosList:#del should start from tail
        oriStr = oriStr[0:subStrIndex:1] + oriStr[subStrIndex+2::1]
    #print(oriStr)
    oriStr = oriStr.replace('\n', '')
    #print(oriStr)
    return oriStr

