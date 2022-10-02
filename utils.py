import os
import PyPDF2
import string
import re
import urllib3
import requests
from bs4 import BeautifulSoup


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
                tempRef = tempAllRefs[tempRefContainer[i]+2+len(str(i+1))::1]
                tempRef = tempRef.strip()
                self.refs.append(tempRef)
            else:
                tempRef = tempAllRefs[tempRefContainer[i]+2+len(str(i+1)):tempRefContainer[i+1]:1]
                tempRef = tempRef.strip()
                self.refs.append(tempRef)

    def ShowRefs(self):
        for ref in self.refs:
            print('--------------------------------------------------------------------------')
            print(ref)

            





def FormatCorrection(oriStr):
    #correct the format for later process
    tempPosList = [subStr.start() for subStr in re.finditer(r'-\n[a-z]', oriStr)]
    #Clear hyphen, but keep en-dash unchanged (hpoefully)
    #print(connectPosList)
    tempPosList = tempPosList[-1::-1]
    for subStrIndex in tempPosList:#del should start from tail
        oriStr = oriStr[0:subStrIndex:1] + oriStr[subStrIndex+2::1]
    tempPosList = [subStr.start() for subStr in re.finditer(r'-\n[A-Z0-9]', oriStr)]
    tempPosList = tempPosList[-1::-1]
    for subStrIndex in tempPosList:#del should start from tail
        oriStr = oriStr[0:subStrIndex+1:1] + oriStr[subStrIndex+2::1]
    #print(oriStr)
    oriStr = oriStr.replace('\n', ' ')
    #print(oriStr)
    return oriStr


def SearchForPaper(paperName):
    #1:Segment name by dot
    tempNamePool = []
    tempPosList = [subStr.start() for subStr in re.finditer(r'\. ', paperName)]
    print(tempPosList)
    for i in range(len(tempPosList)):
        if i == len(tempPosList) - 1:
            tempStr = paperName[tempPosList[i]+1::1]
            tempStr = tempStr.strip()
            tempNamePool.append(tempStr)
        else:
            tempStr = paperName[tempPosList[i]+1:tempPosList[i+1]:1]
            tempStr = tempStr.strip()
            tempNamePool.append(tempStr)
    tempNamePool = tempNamePool[-1::-1]
    print(tempNamePool)
    for segName in tempNamePool:
        #http = urllib3.PoolManager()
        #response = http.request('GET', 'https://dblp.org/search?q=' + segName)
        ##print(response.status,response.data.decode('utf-8'))
        #data = response.data.decode('utf-8')
        url = 'https://dblp.org/search?q=' + segName
        bs = BeautifulSoup(requests.get(url).content, "lxml")
        result = bs.find('p', id = "completesearch-info-matches").get_text()
        print(result)
        #searched = bs.find(class_ = "publ-list")
        #ul = searched.find('ul')
        #print(ul)
        #print(response.data.decode('utf-8'))
