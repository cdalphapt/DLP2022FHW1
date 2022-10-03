# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainTvpjiU.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_mainUI(object):
    def setupUi(self, mainUI):
        if not mainUI.objectName():
            mainUI.setObjectName(u"mainUI")
        mainUI.resize(640, 502)
        self.cmdOutput = QTextBrowser(mainUI)
        self.cmdOutput.setObjectName(u"cmdOutput")
        self.cmdOutput.setGeometry(QRect(10, 170, 621, 311))
        self.pdfSelectButton = QPushButton(mainUI)
        self.pdfSelectButton.setObjectName(u"pdfSelectButton")
        self.pdfSelectButton.setGeometry(QRect(520, 30, 101, 28))
        self.progressBar = QProgressBar(mainUI)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(10, 140, 621, 23))
        self.progressBar.setValue(24)
        self.pdfDirShower = QTextBrowser(mainUI)
        self.pdfDirShower.setObjectName(u"pdfDirShower")
        self.pdfDirShower.setGeometry(QRect(10, 30, 501, 31))
        self.paperInfoShower = QTextBrowser(mainUI)
        self.paperInfoShower.setObjectName(u"paperInfoShower")
        self.paperInfoShower.setGeometry(QRect(10, 70, 501, 61))
        self.startSearchButton = QPushButton(mainUI)
        self.startSearchButton.setObjectName(u"startSearchButton")
        self.startSearchButton.setGeometry(QRect(520, 80, 101, 41))
        self.label = QLabel(mainUI)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(180, 10, 291, 16))
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(mainUI)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(500, 480, 131, 20))
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_3 = QLabel(mainUI)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 480, 131, 20))

        self.retranslateUi(mainUI)

        QMetaObject.connectSlotsByName(mainUI)
    # setupUi

    def retranslateUi(self, mainUI):
        mainUI.setWindowTitle(QCoreApplication.translate("mainUI", u"PDF PP", None))
        self.pdfSelectButton.setText(QCoreApplication.translate("mainUI", u"Select PDF", None))
        self.startSearchButton.setText(QCoreApplication.translate("mainUI", u"Download", None))
        self.label.setText(QCoreApplication.translate("mainUI", u"Simple PDF PaperReference Processor", None))
        self.label_2.setText(QCoreApplication.translate("mainUI", u"made by CDalpha", None))
        self.label_3.setText(QCoreApplication.translate("mainUI", u"v1.0    20221003", None))
    # retranslateUi

