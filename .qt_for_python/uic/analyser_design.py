# Form implementation generated from reading ui file 'd:\Viewer\analyser_design.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setMinimumSize(QtCore.QSize(1920, 1080))
        MainWindow.setMaximumSize(QtCore.QSize(1920, 1080))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 230, 1901, 841))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1899, 839))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.ScreenshotLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.ScreenshotLabel.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.ScreenshotLabel.setText("")
        self.ScreenshotLabel.setObjectName("ScreenshotLabel")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.FindBtn = QtWidgets.QPushButton(self.centralwidget)
        self.FindBtn.setGeometry(QtCore.QRect(1810, 10, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.FindBtn.setFont(font)
        self.FindBtn.setObjectName("FindBtn")
        self.FindResult = QtWidgets.QListWidget(self.centralwidget)
        self.FindResult.setGeometry(QtCore.QRect(10, 50, 1901, 171))
        self.FindResult.setObjectName("FindResult")
        self.FindPlane = QtWidgets.QLineEdit(self.centralwidget)
        self.FindPlane.setGeometry(QtCore.QRect(10, 10, 1791, 31))
        self.FindPlane.setObjectName("FindPlane")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Analyser"))
        self.FindBtn.setText(_translate("MainWindow", "??????????"))
