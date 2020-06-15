# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(563, 436)
        self.pushButton_2 = QtWidgets.QPushButton(Frame)
        self.pushButton_2.setGeometry(QtCore.QRect(450, 70, 80, 26))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(Frame)
        self.pushButton.setGeometry(QtCore.QRect(450, 20, 80, 26))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Frame)
        self.label.setGeometry(QtCore.QRect(14, 20, 91, 20))
        self.label.setObjectName("label")
        self.lineEdit_2 = QtWidgets.QLineEdit(Frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(140, 70, 261, 26))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(Frame)
        self.label_2.setGeometry(QtCore.QRect(14, 70, 91, 20))
        self.label_2.setObjectName("label_2")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Frame)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 120, 521, 291))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.comboBox = QtWidgets.QComboBox(Frame)
        self.comboBox.setGeometry(QtCore.QRect(141, 20, 261, 26))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.pushButton_2.setText(_translate("Frame", "Predict"))
        self.pushButton.setText(_translate("Frame", "Train"))
        self.label.setText(_translate("Frame", "Current Weather"))
        self.label_2.setText(_translate("Frame", "Future Weather"))
        self.comboBox.setItemText(0, _translate("Frame", "新建项目"))
        self.comboBox.setItemText(1, _translate("Frame", "2"))
        self.comboBox.setItemText(2, _translate("Frame", "3"))
        self.comboBox.setItemText(3, _translate("Frame", "4"))

