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
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Frame)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 120, 521, 291))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.comboBox = QtWidgets.QComboBox(Frame)
        self.comboBox.setGeometry(QtCore.QRect(141, 20, 261, 26))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("Rain")
        self.comboBox.addItem("Fog-Rain-Snow")
        self.comboBox.addItem("Fog-Snow")
        self.comboBox.addItem("Normal")
        self.comboBox.addItem("Rain-Snow")
        self.comboBox.addItem("Fog-Rain")
        self.comboBox.addItem("Snow")
        self.comboBox.addItem("Fog")
        self.comboBox.addItem("Rain-Thunderstorm")
        self.label = QtWidgets.QLabel(Frame)
        self.label.setGeometry(QtCore.QRect(14, 20, 91, 20))
        self.label.setObjectName("label")
        self.lineEdit_2 = QtWidgets.QLineEdit(Frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(140, 70, 261, 26))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(Frame)
        self.label_2.setGeometry(QtCore.QRect(14, 70, 91, 20))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.pushButton_2.setText(_translate("Frame", "Predict"))
        self.pushButton.setText(_translate("Frame", "Train"))
        self.pushButton.clicked.connect(self.train_clicked)
        self.pushButton_2.clicked.connect(self.pred_clicked)
        self.label.setText(_translate("Frame", "Current Weather"))
        self.label_2.setText(_translate("Frame", "Future Weather"))

    def train_clicked(self):
        from main_model import HMM, weather_data_gene
        get_text = self.plainTextEdit.toPlainText()
        self.plainTextEdit.setPlainText("Training Model, Please wait a minute...")
        self.O, self.A, self.B, self.Pi, self.h_dict, self.o_len, self.h_len = weather_data_gene(src_text=get_text)
        epoch = 8
        self.model = HMM()
        self.A, self.B, self.Pi = self.model.Learning(self.O, self.A, self.B, self.Pi, self.h_dict, epoch)
        self.plainTextEdit.setPlainText("Training Model Finished")

    def pred_clicked(self):
        get_text = self.comboBox.currentText()
        get_id = self.h_dict[get_text]
        pred_id = self.model.predict(get_id)
        for k, v in self.h_dict.items():
            if v == pred_id:
                self.lineEdit_2.setText(k)
                return