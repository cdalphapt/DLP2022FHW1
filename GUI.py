from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from threading import Thread
from PySide2.QtCore import Signal,QObject
import tkinter as tk
from tkinter import filedialog
import utils


ui = None
window = None

#class UndateDownloadSignal(QObject):
#    sinOut = Signal(str, int, int)

#global_sin = UndateDownloadSignal()   

class DownloadBibThread(QObject):
    sinOut = Signal(str, int, int)
 
    def __init__(self):
        super(DownloadBibThread, self).__init__()
        pass
 
    def run():
        tempCMDOutput = 'Start downloading bib files of refs......\n'
        ui.cmdOutput.setPlainText(tempCMDOutput)
        self.sinOut.emit(tempCMDOutput,0,len(window.pdfPaper.refs))
        for i in range(len(window.pdfPaper.refs)):
            tempCMDOutput = utils.SearchForPaper(window.pdfPaper.refs[i])
            self.sinOut.emit(tempCMDOutput,i,len(window.pdfPaper.refs))
        pass

def DownloadUpdate(tempCMDOutput,i,total):
    ui.cmdOutput.setPlainText(tempCMDOutput)
    ui.progressBar.setValue((i+1)/total)



class interactiveWindow:
    def __init__(self):
        self.pdfDir = ''
        self.pdfPaper = None
        self.ui = QUiLoader().load('./UIrelated/main.ui')
        self.ui.pdfSelectButton.clicked.connect(self.ChoosePdf)
        self.ui.startSearchButton.clicked.connect(self.DownloadRefsBib)
        self.ui.progressBar.setValue(0)

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
        #Thread = DownloadBibThread()
        #DownloadBibThread.run()
        #DownloadBibThread.sinOut.connect(DownloadUpdate)
        #Maybe the pdf is normal state now.
        tempCMDOutput = 'Start downloading bib files of refs......\n'
        self.ui.cmdOutput.setPlainText(tempCMDOutput)
        for i in range(len(self.pdfPaper.refs)):
            tempCMDOutput += utils.SearchForPaper(self.pdfPaper.refs[i])
            self.ui.cmdOutput.setPlainText(tempCMDOutput)
            self.ui.progressBar.setValue(100 * (i+1) / len(self.pdfPaper.refs))



def InitWindow():
    app = QApplication([])
    iWin = interactiveWindow();
    iWin.ui.show()
    app.exec_()
    return iWin


