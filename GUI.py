from PySide2.QtWidgets import QApplication,QWidget,QPlainTextEdit,QProgressBar,QMainWindow
from PySide2.QtUiTools import QUiLoader
from threading import Thread
from PySide2.QtCore import Signal,QObject
import tkinter as tk
from tkinter import filedialog
import utils
from mainUI import Ui_mainUI


#ui = None
#window = None

##class UndateDownloadSignal(QObject):
##    sinOut = Signal(str, int, int)

##global_sin = UndateDownloadSignal()   

#class DownloadBibThread(QObject):
#    sinOut = Signal(str, int, int)
 
#    def __init__(self):
#        super(DownloadBibThread, self).__init__()
#        pass
 
#    def run():
#        tempCMDOutput = 'Start downloading bib files of refs......\n'
#        ui.cmdOutput.setPlainText(tempCMDOutput)
#        self.sinOut.emit(tempCMDOutput,0,len(window.pdfPaper.refs))
#        for i in range(len(window.pdfPaper.refs)):
#            tempCMDOutput = utils.SearchForPaper(window.pdfPaper.refs[i])
#            self.sinOut.emit(tempCMDOutput,i,len(window.pdfPaper.refs))
#        pass

#def DownloadUpdate(tempCMDOutput,i,total):
#    ui.cmdOutput.setPlainText(tempCMDOutput)
#    ui.progressBar.setValue((i+1)/total)

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
        thread = Thread(target=self.DownloadRefsBibThreadFunc)
        thread.start()
        #Maybe the pdf is normal state now.
        #tempCMDOutput = 'Start downloading bib files of refs......\n'
        #self.ui.cmdOutput.setPlainText(tempCMDOutput)
        #for i in range(len(self.pdfPaper.refs)):
        #    tempCMDOutput += utils.SearchForPaper(self.pdfPaper.refs[i])
        #    self.ui.cmdOutput.setPlainText(tempCMDOutput)
        #    self.ui.progressBar.setValue(100 * (i+1) / len(self.pdfPaper.refs))

    def DownloadRefsBibThreadFunc(self):
        tempCMDOutput = 'Start downloading bib files of refs......\n'
        tempLen = len(self.pdfPaper.refs)
        successNum = 0
        self.dSignal.dSignal.emit(self.ui.cmdOutput, self.ui.progressBar, tempCMDOutput, 0)
        #self.ui.cmdOutput.setPlainText(tempCMDOutput)
        for i in range(tempLen):
            tempCMDOutput += utils.SearchForPaper(self.pdfPaper.refs[i])
            if tempCMDOutput[-5:-1:1] == '.bib':
                successNum += 1
            self.dSignal.dSignal.emit(self.ui.cmdOutput, self.ui.progressBar, tempCMDOutput, 100 * (i+1) / tempLen)
        tempCMDOutput += '----------------------------------------\nDownload Finished:\n'
        tempCMDOutput += 'Total: '+str(tempLen)+'    Success:'+str(successNum)+'    Fail:'+str(tempLen-successNum)+'    SDRatio:'+str(int(100*successNum/tempLen))+"%\n"
        self.dSignal.dSignal.emit(self.ui.cmdOutput, self.ui.progressBar, tempCMDOutput, 100)
        #self.ui.cmdOutput.setPlainText(tempCMDOutput)
        #self.ui.progressBar.setValue(100 * (i+1) / tempLen)

    def ReceiveDownloadSignal(self, pt, pb, textStr, progInt):
        pt.setPlainText(textStr)
        pb.setValue(progInt)



def InitWindow():
    app = QApplication([])
    iWin = interactiveWindow();
    iWin.show()
    app.exec_()
    return iWin


