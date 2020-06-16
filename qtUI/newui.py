# -*- coding: utf-8 -*-
# --//                            _ooOoo_
# --//                           o8888888o
# --//                           88" . "88
# --//                           (| -_- |)
# --//                            O\ = /O
# --//                        ____/`---'\____
# --//                      .   ' \\| |// `.
# --//                       / \\||| : |||// \
# --//                     / _||||| -:- |||||- \
# --//                       | | \\\ - /// | |
# --//                     | \_| ''\---/'' | |
# --//                      \ .-\__ `-` ___/-. /
# --//                   ___`. .' /--.--\ `. . __
# --//                ."" '< `.___\_<|>_/___.' >'"".
# --//               | | : `- \`.;`\ _ /`;.`/ - ` : | |
# --//                 \ \ `-. \_ __\ /__ _/ .-` / /
# --//         ======`-.____`-.___\_____/___.-`____.-'======
# --//                            `=---='
# --//
# --//         .............................................
# --//                  佛祖保佑             永无BUG

# Form implementation generated from reading ui file 'UI.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(563, 500)
        self.pushButton_2 = QtWidgets.QPushButton(Frame)
        self.pushButton_2.setGeometry(QtCore.QRect(450, 70, 80, 26))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(Frame)
        self.pushButton.setGeometry(QtCore.QRect(450, 20, 80, 26))
        self.pushButton.setObjectName("pushButton")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Frame)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 170, 521, 291))
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
        self.lineEdit_3 = QtWidgets.QLineEdit(Frame)
        self.lineEdit_3.setGeometry(QtCore.QRect(140, 120, 261, 26))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_2 = QtWidgets.QLabel(Frame)
        self.label_2.setGeometry(QtCore.QRect(14, 70, 91, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Frame)
        self.label_3.setGeometry(QtCore.QRect(14, 120, 91, 20))
        self.label_3.setObjectName("label_3")
        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)
        self.trained = False

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.pushButton_2.setText(_translate("Frame", "Predict"))
        self.pushButton.setText(_translate("Frame", "Train"))
        self.pushButton.clicked.connect(self.train_clicked)
        self.pushButton_2.clicked.connect(self.pred_clicked)
        self.label.setText(_translate("Frame", "Current  Weather"))
        self.label_2.setText(_translate("Frame", "Future  Weather"))
        self.label_3.setText(_translate("Frame", "Training Epochs"))
        self.lineEdit_3.setText("50")

    def train_clicked(self):
        from main_model import HMM, weather_data_gene
        if not self.trained:
            self.get_text = self.plainTextEdit.toPlainText()
            self.trained = True
        self.plainTextEdit.setPlainText("Training Model, Please wait a minute...")
        epoch = int(self.lineEdit_3.text())
        self.O, self.A, self.B, self.Pi, self.h_dict, self.o_len, self.h_len = weather_data_gene(src_text=self.get_text)
        self.model = HMM()
        self.A, self.B, self.Pi = self.model.Learning(self.O, self.A, self.B, self.Pi, self.h_dict, epoch)
        self.plainTextEdit.appendPlainText("Training Model Finished")
        self.src_O = self.O[0]
        self.pred_O = self.model.predict_all(self.src_O)
        self.pred_O = self.model.find_map(self.pred_O, self.src_O, 9)
        self.plainTextEdit.appendPlainText("Test Model:")
        self.plainTextEdit.appendPlainText("Source Observer Data:")
        self.plainTextEdit.appendPlainText(" ".join([str(num) for num in self.src_O[40:80]]))
        self.plainTextEdit.appendPlainText("Predict Observer Data:")
        self.plainTextEdit.appendPlainText(" ".join([str(num) for num in self.pred_O[40:80]]))
        self.plainTextEdit.appendPlainText("Total Accuracy:")
        total_equal = sum([(1 if self.src_O[i] == self.pred_O[i] else 0) for i in range(len(self.src_O))])
        self.plainTextEdit.appendPlainText(str(100 * total_equal/len(self.src_O)) + "%")


    def pred_clicked(self):
        get_text = self.comboBox.currentText()
        get_id = self.h_dict[get_text]
        pred_id = self.model.predict(get_id)
        for k, v in self.h_dict.items():
            if v == pred_id:
                self.lineEdit_2.setText(k)
                return