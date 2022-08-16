
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt

# 클래스 OOP
class qTemplate(QWidget):
    # 생성자
    def __init__(self) -> None:      #class 이므로 self : qtpy 본인을 뜻한다. 함수 후 return을 해야하는데, 이 경우 '생성자'이므로 None: return 값이 없다.
        super().__init__()
        self.initUI()

# 화면 정의를 위해 사용자 함수
    def initUI(self) -> None:
        self.addControls()
        self.setGeometry(300, 100, 640, 400)     
        self.setWindowTitle('QPushbutton')
        self.show()

    def addControls(self) -> None:
        self.btn1 = QPushButton('Click', self)
        self.btn1.setGeometry(500, 350, 120, 40)
        self.btn1.clicked.connect(self.btn1_clicked)   # 시그널 연결
        self.label = QLabel('메세지:', self)

    # click: 클릴할 때   clicked: 클릭 후 손을 뗐을 때 
    # event = signal (python)
    def btn1_clicked(self):
        self.label.setText('메세지 : btnl 버튼 클릭 !')
        QMessageBox.information(self, 'signal','Button clicked!!' ) # 일반정보창 # 메세지박스 안의 제목: signal,  클릭 누르면 'Button clicked!!'글이 나온다.
    #   QMessageBox.Warning(self, 'signal','Button clicked!!' )     # 경고창 표시가 뜬다.
    #   QMessageBox.critical(self, 'signal','Button clicked!!' )    # 에러창 표시가 뜬다.





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qTemplate()
    app.exec_()


