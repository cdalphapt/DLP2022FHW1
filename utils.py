from base64 import encode
import os
from urllib import request
import PyPDF2
import string
import re
import urllib3
import requests
from bs4 import BeautifulSoup
import time
from main import debug      

foundStr = ['found one match','found 2 matches', 'found 3 matches', 'found 4 matches', 'found 5 matches']


class pdfPaper:
    #The class contains basic info about the paper. (e.g title, ref, etc.)
    def __init__(self, dir):
        self.dir = dir
        pdfReader = PyPDF2.PdfFileReader(open(dir, 'rb'))
        self.title = pdfReader.getDocumentInfo().title
        print(self.title)
        self.contentTxt = ""
        self.refs = []
        for page in pdfReader.pages:
            self.contentTxt += page.extract_text()
        if debug == 1:
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

    def DownloadAllPapers(self):
        for ref in self.refs:
            SearchForPaper(ref)

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
    print('--------------------------------------------------------------------------')
    print("Downloading:\n" + paperName)
    tempNamePool = []
    tempPosList = [subStr.start() for subStr in re.finditer(r'\. ', paperName)]
    if debug == 1:
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
    if debug == 1:
        print(tempNamePool)
    IsFindPaper = 0
    for segName in tempNamePool:
        #http = urllib3.PoolManager()
        #response = http.request('GET', 'https://dblp.org/search?q=' + segName)
        ##print(response.status,response.data.decode('utf-8'))
        #data = response.data.decode('utf-8')
        url = 'https://dblp.org/search?q=' + segName
        bs = BeautifulSoup(requests.get(url).content, "lxml")
        result = bs.find('p', id = 'completesearch-info-matches').get_text()
        if debug == 1:
            print(result)
        if not foundStr.__contains__(result):
            continue
        else:
            ul_1 = bs.find('ul', class_ = 'publ-list')
            nav = ul_1.find('nav', class_ = 'publ')
            navTxt = str(nav)
            #find BibTex
            texPos = navTxt.find("BibTeX")
            closeAStart,closeAEnd = len(navTxt),len(navTxt)
            #Find <a></a> bibtex belong
            for subStr in re.finditer('<a', navTxt[0:texPos:1]):
                if abs(subStr.start() - texPos) <= abs(closeAStart - texPos):
                    closeAStart = subStr.start()
            for subStr in re.finditer('</a>', navTxt[texPos::1]):
                if abs(subStr.start()) <= abs(closeAEnd):
                    closeAEnd = subStr.start()
            subBibTeXStr = navTxt[closeAStart:closeAEnd+texPos:1]
            herfPos = subBibTeXStr.find("href=")
            linkS,linkE = -1,-1
            i = herfPos
            for char in subBibTeXStr[herfPos::1]:
                i += 1
                if char == '\"':
                    if linkS == -1:
                        linkS = i
                    elif linkE == -1:
                        linkE = i
                        break
            herfLink = subBibTeXStr[linkS:linkE-1:1]
            #find bib download link
            bibWeb = str(BeautifulSoup(requests.get(herfLink).content, "lxml"))
            texPos = str(bibWeb).find("download as .bib file")
            closeAStart,closeAEnd = len(bibWeb),len(bibWeb)
            #Find <a></a> bib belong
            for subStr in re.finditer('<a', bibWeb[0:texPos:1]):
                if abs(subStr.start() - texPos) <= abs(closeAStart - texPos):
                    closeAStart = subStr.start()
            for subStr in re.finditer('</a>', bibWeb[texPos::1]):
                if abs(subStr.start()) <= abs(closeAEnd):
                    closeAEnd = subStr.start()
            subBibTeXStr = bibWeb[closeAStart:closeAEnd+texPos:1]
            herfPos = subBibTeXStr.find("href=")
            linkS,linkE = -1,-1
            i = herfPos
            for char in subBibTeXStr[herfPos::1]:
                i += 1
                if char == '\"':
                    if linkS == -1:
                        linkS = i
                    elif linkE == -1:
                        linkE = i
                        break
            bibDownloadLink = subBibTeXStr[linkS:linkE-1:1]
            bib = requests.get(bibDownloadLink)
            f = open('./download/' + str(time.time()) + '.bib', 'wb')
            f.write(bib.content)
            f.close()
            print("Download Success")
            IsFindPaper = 1
            return 1;
    if IsFindPaper == 0:
        print("Paper not Found")
        return 0;


            #bibPos = nav.

            #print(bibPos)
        #Find the only paper suitable
        

        #searched = bs.find(class_ = "publ-list")
        #ul = searched.find('ul')
        #print(ul)
        #print(response.data.decode('utf-8'))
