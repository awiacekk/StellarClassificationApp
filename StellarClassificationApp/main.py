
import sys
from threading import Thread

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox

from neural import Neural


class UiMainWindow:
    def __init__(self):
        self.i = 0
        self.movie = None
        self.tab = {'alpha': [0], 'delta': [0], 'u': [0], 'g': [0], 'r': [0], 'i': [0], 'z': [0],
                    'spec_obj_ID': [0], 'redshift': [0], 'plate': [0], 'MJD': [0]}
        self.name_tab = {'KNN': [''], 'Neural': ['']}
        self.name_tab_later = {'KNN': [''], 'Neural Network': ['']}
        self.obj = Neural("")
        self.flag = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1525, 600)
        MainWindow.setWindowIcon(QtGui.QIcon('icon.png'))
        MainWindow.setFixedSize(MainWindow.size())
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(55, 0, 1455, 81))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout_2.addWidget(self.label_2)
        self.comboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("KNN")
        self.comboBox.addItem("Neural Network")
        self.comboBox.currentTextChanged.connect(self.changedIndex)
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.loadCsv)
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout_2.addWidget(self.label)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 80, 1525, 431))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.table = QtWidgets.QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels(["klasyfikacja", "alpha", "delta", "u", "g", "r", "i", "z", "spec_obj_ID",
                                              "redshift", "plate", "MJD"])
        self.fillZeros()
        self.table.itemChanged.connect(self.changedCell)
        self.horizontalLayout_3.addWidget(self.table)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(1400, 520, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.addRow)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(400, 520, 93, 28))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(732, 530, 30, 30))
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Stellar Classification"))
        self.pushButton.setText(_translate("MainWindow", "Wybierz plik *.csv"))
        self.label.setText(_translate("MainWindow", ""))
        self.label_2.setText(_translate("MainWindow", "Wybierz model:"))
        self.pushButton_3.setText(_translate("MainWindow", "Dodaj wiersz"))
        self.label_3.setText(_translate("MainWindow", ""))

    def loadCsv(self):
        file, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                  "", "Microsoft Excel Files (*.csv)")
        if check:
            url = QUrl.fromLocalFile(file)
            self.label.setText(url.fileName())
            file = file.replace("/", "\\")
            self.obj.set_file(file)
            thread1 = Thread(target=self.learnFromFileKNN)
            thread2 = Thread(target=self.learnFromFileNeural)
            thread1.start()
            thread2.start()
            self.movie = QMovie("loading.gif")
            self.label_4.setMovie(self.movie)
            self.movie.start()

    def learnFromFileKNN(self):
        self.obj.calculateKNN()
        self.i += 1
        if self.i == 2:
            self.movie.stop()
            movie = QMovie()
            self.label_4.setMovie(movie)

    def learnFromFileNeural(self):
        self.obj.calculateNeural()
        self.i += 1
        if self.i == 2:
            self.movie.stop()
            movie = QMovie()
            self.label_4.setMovie(movie)

    def changedIndex(self):
        self.flag = True
        label = self.comboBox.currentText()
        if self.table.rowCount() > 1:
            for row in range(len(self.name_tab_later[label])-1):
                item = self.name_tab_later[label][row+1]
                self.table.setItem(row, 0, QTableWidgetItem(item))
                self.table.item(row, 0).setBackground(QtGui.QColor(212, 219, 255))
            self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem(self.name_tab[label][0]))
            self.table.item(self.table.rowCount()-1, 0).setBackground(QtGui.QColor(212, 219, 255))
        else:
            item = self.name_tab[label][0]
            row = self.table.rowCount()-1
            self.table.setItem(row, 0, QTableWidgetItem(item))
            self.table.item(row, 0).setBackground(QtGui.QColor(212, 219, 255))
        self.flag = False

    def changedCell(self):
        number = True
        if not self.flag:
            for col in range(self.table.columnCount() - 1):
                if not self.isNumber(self.table.item(self.table.rowCount() - 1, col + 1).text()):
                    number = False
                    break
                self.tab[self.table.horizontalHeaderItem(col + 1).text()] = [
                    float(self.table.item(self.table.rowCount() - 1, col + 1).text())]

            if number and self.i == 2:
                thread = Thread(target=self.classification)
                thread.start()
            elif not number:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Niepoprawne dane")
                msg.setInformativeText('Podaj wartosc liczbowa')
                msg.setWindowTitle("Blad")
                msg.exec_()

    def isNumber(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    def fillZeros(self):
        self.flag = True
        row = self.table.rowCount() - 1

        for col in range(self.table.columnCount()-1):
            self.table.setItem(row, col + 1, QTableWidgetItem("0"))

        self.table.setItem(row, 0, QTableWidgetItem(" "))
        self.table.item(row, 0).setBackground(QtGui.QColor(212, 219, 255))
        self.flag = False

    def classification(self):
        pred = self.obj.classificateKNN(self.tab)
        self.name_tab['KNN'] = [pred]
        if self.comboBox.currentText() == "KNN":
            self.table.setItem(self.table.rowCount() - 1, 0, QTableWidgetItem(pred))
        self.table.item(self.table.rowCount() - 1, 0).setBackground(QtGui.QColor(212, 219, 255))

        pred = self.obj.classificateNeural(self.tab)
        self.name_tab['Neural Network'] = [pred]
        if self.comboBox.currentText() == "Neural Network":
            self.table.setItem(self.table.rowCount() - 1, 0, QTableWidgetItem(pred))
        self.table.item(self.table.rowCount() - 1, 0).setBackground(QtGui.QColor(212, 219, 255))

    def addRow(self):
        current_row = self.table.rowCount()
        self.table.insertRow(current_row)
        self.fillZeros()
        self.tab = {'alpha': [0], 'delta': [0], 'u': [0], 'g': [0], 'r': [0], 'i': [0], 'z': [0],
                    'spec_obj_ID': [0], 'redshift': [0], 'plate': [0], 'MJD': [0]}
        self.name_tab_later['KNN'].append(self.name_tab['KNN'][0])
        self.name_tab_later['Neural Network'].append(self.name_tab['Neural Network'][0])


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
