import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication,QPushButton,QLineEdit
from PySide6.QtCore import QFile, QIODevice,Slot


@Slot()
def sendPara(self):
    print( float(window.findChild(QLineEdit,"lineEdit").text())+0.1)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui_file_name = "para.ui"
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
    window.show()
    #window.findChild(QPushButton,"pushButton").clicked.connect(sendPara)
    sys.exit(app.exec_())