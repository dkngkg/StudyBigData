
import sys
from PyQt5 import uic 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt

# 클래스 OOP
class qTemplate(QWidget):
    # 생성자
    def __init__(self) -> None:      #class 이므로 self : qtpy 본인을 뜻한다. 함수 후 return을 해야하는데, 이 경우 '생성자'이므로 None: return 값이 없다.
        super().__init__()
        uic.loadUi('./pyqt02/ttask.ui', self)
        self.initUI()

# 화면 정의를 위해 사용자 함수
    def initUI(self) -> None:
        self.addControls()
        self.show()

    def addControls(self) -> None:
        self.btnStart.clicked.connect(self.btn1_clicked)   # 시그널 연결

    # click: 클릴할 때   clicked: 클릭 후 손을 뗐을 때 
    # event = signal (python)
    def btn1_clicked(self):
        self.txbLog.append('실행!!')
        self.pgbTask.setRange(0,999999) 
        for i in range(0, 1000000):     # 스레드 처리를 못해서 "응답없음" 발생
            print(f'출력: {i}')
            self.pgbTask.setValue(i)
            self.txbLog.append(f'출력 > {i}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qTemplate()
    app.exec_()


