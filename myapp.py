import sys
from PyQt5.QtWidgets import *
import demo as ya
from PyQt5.QtCore import *

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        # self.lbl1 = QLabel('파일명:', self)
        self.lbl2 = QLabel('', self)
        # self.le = QLineEdit(self)
        self.datetimeedit = QDateTimeEdit(self)
        self.datetimeedit.setDateTime(QDateTime.currentDateTime())
        self.datetimeedit.setDateTimeRange(QDateTime(1900, 1, 1, 00, 00, 00), QDateTime(2100, 1, 1, 00, 00, 00))
        self.datetimeedit.setDisplayFormat('yyyy.MM.dd hh:00:00')
        self.trans_btn = QPushButton('ADD', self)
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        # vbox.addWidget(self.lbl1)
        # vbox.addWidget(self.le)
        vbox.addWidget(self.datetimeedit)
        vbox.addWidget(self.trans_btn)
        vbox.addWidget(self.lbl2)
        self.setLayout(vbox)

        self.trans_btn.clicked.connect(self.translate)
        # self.le.editingFinished.connect(self.translate_kor)

        self.setWindowTitle('Video Information')
        self.setGeometry(300, 300, 400, 200)
        self.show()

    def translate(self):
        # link = self.le.text()
        time = self.datetimeedit.dateTime().toString("yyyy-MM-ddThh:mm:ssZ")
        # print(time)
        # print(link)
        # text = ya.video2excel(link, time)
        text = ya.video2excel(time)

        self.lbl2.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    