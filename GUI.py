from PySide2.QtWidgets import QApplication,QWidget,QPlainTextEdit,QProgressBar,QMainWindow
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Signal,QObject
from threading import Thread
import tkinter as tk
from tkinter import filedialog
import utils
from mainUI import Ui_mainUI


class DownloadUpdateSignals(QObject):
    dSignal = Signal(QPlainTextEdit, QProgressBar, str, int)

class interactiveWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.pdfDir = ''
        self.pdfPaper = None
        self.ui = Ui_mainUI()
        self.ui.setupUi(self)
        self.ui.pdfSelectButton.clicked.connect(self.ChoosePdf)
        self.ui.startSearchButton.clicked.connect(self.DownloadRefsBib)
        self.ui.progressBar.setValue(0)
        self.dSignal = DownloadUpdateSignals()
        self.dSignal.dSignal.connect(self.ReceiveDownloadSignal)

    def ChoosePdf(self):
        root = tk.Tk()
        root.withdraw()
        self.pdfDir = filedialog.askopenfilename()
        if not self.pdfDir[-4::1] == '.pdf':
            self.pdfDir = ''
            self.ui.pdfDirShower.setPlainText("Please Select PDF file.")
        else:
            self.ui.pdfDirShower.setPlainText(self.pdfDir)
            self.pdfPaper = utils.pdfPaper(self.pdfDir)
            self.ui.paperInfoShower.setPlainText(self.pdfPaper.title)
            self.ui.cmdOutput.setPlainText(self.pdfPaper.ShowRefs())

    def DownloadRefsBib(self):
        if self.pdfDir == '' or self.pdfPaper == None:
            return
        #Maybe the pdf is normal state now.
        thread = Thread(target=self.DownloadRefsBibThreadFunc)
        thread.start()       
        ### Non-multithreading
        #tempCMDOutput = 'Start downloading bib files of refs......\n'
        #self.ui.cmdOutput.setPlainText(tempCMDOutput)
        #for i in range(len(self.pdfPaper.refs)):
        #    tempCMDOutput += utils.SearchForPaper(self.pdfPaper.refs[i])
        #    self.ui.cmdOutput.setPlainText(tempCMDOutput)
        #    self.ui.progressBar.setValue(100 * (i+1) / len(self.pdfPaper.refs))
        ###

    def DownloadRefsBibThreadFunc(self):
        #Thread for updating download info
        tempCMDOutput = 'Start downloading bib files of refs......\n'
        tempLen = len(self.pdfPaper.refs)
        successNum = 0
        self.dSignal.dSignal.emit(self.ui.cmdOutput, self.ui.progressBar, tempCMDOutput, 0)
        for i in range(tempLen):
            tempCMDOutput += utils.SearchForPaper(self.pdfPaper.refs[i])
            if tempCMDOutput[-5:-1:1] == '.bib':
                successNum += 1
            self.dSignal.dSignal.emit(self.ui.cmdOutput, self.ui.progressBar, tempCMDOutput, 100 * (i+1) / tempLen)
        tempCMDOutput += '----------------------------------------\nDownload Finished:\n'
        tempCMDOutput += 'Total: '+str(tempLen)+'    Success:'+str(successNum)+'    Fail:'+str(tempLen-successNum)+'    SDRatio:'+str(int(100*successNum/tempLen))+"%\n"
        self.dSignal.dSignal.emit(self.ui.cmdOutput, self.ui.progressBar, tempCMDOutput, 100)

    def ReceiveDownloadSignal(self, pt, pb, textStr, progInt):
        pt.setPlainText(textStr)
        pb.setValue(progInt)



def InitWindow():
    app = QApplication([])
    iWin = interactiveWindow();
    iWin.show()
    app.exec_()
    return iWin


