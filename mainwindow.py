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
import sys
from PyQt5.QtWidgets import QApplication, QWidget #导入相应的包
from PyQt5.QtWidgets import QApplication , QMainWindow
from qtUI.newui import *


""" 主函数 """
app = QApplication(sys.argv)
#app = QApplication(sys.argv)，每一个pyqt程序必须创建一个application对象， #sys.argv是命令行参数，可以通过命令启动的时候传递参数。
mainWindow = QMainWindow() #生成过一个实例（对象）,
# mainWindow是实例（对象）的名字，可以随便起。
ui = Ui_Frame()
ui.setupUi(mainWindow)
mainWindow.show() #用来显示窗口
sys.exit(app.exec_())#exec_()方法的作用是“进入程序的主循环直到exit()被调