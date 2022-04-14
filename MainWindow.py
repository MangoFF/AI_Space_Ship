import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication,QPushButton,QLineEdit
from PySide6.QtCore import QFile, QIODevice,Slot
from plane import rungame,tech,AI_play,ship_labeling,train_model,remoeModel,removeData
import random
@Slot()
def sendPara(self):
    print( float(window.findChild(QLineEdit,"lineEdit").text())+0.1)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui_file_name = "mainwindow.ui"
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        sys.exit(-1)
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)
    window.findChild(QPushButton,"kaishiyouxi").clicked.connect(rungame)
    window.findChild(QPushButton, "shoudongbiaoji").clicked.connect(ship_labeling)
    window.findChild(QPushButton, "gensuixuexi").clicked.connect(tech)
    window.findChild(QPushButton, "youjianduxunlian").clicked.connect(train_model)
    window.findChild(QPushButton, "AI_PLAY").clicked.connect(AI_play)

    window.findChild(QPushButton, "rmdata").clicked.connect(removeData)
    window.findChild(QPushButton, "rmmodel").clicked.connect(remoeModel)
    window.show()
    app.exec()