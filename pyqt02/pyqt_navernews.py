
import sys
from PyQt5 import uic 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
from PyQt5.QtCore import *
import time


# UI 스레드와 작업스레드 분리
class Worker(QThread): 
    # QThread는 화면을 그릴 권한이 없음
    # 대신 통신을 통해서 UI 스레드가 그림을 그릴 수 있도록 통신 수행.
    valChangeSignal = pyqtSignal(int)


# 클래스 OOP
class qTemplate(QWidget):
    # 생성자
    def __init__(self) -> None:      #class 이므로 self : qtpy 본인을 뜻한다. 함수 후 return을 해야하는데, 이 경우 '생성자'이므로 None: return 값이 없다.
        super().__init__()
        uic.loadUi('./pyqt02/navernews.ui', self)
        self.initUI()



    def addControls(self) -> None:
        pass
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qTemplate()
    app.exec_()


