
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



    def __init__(self, parent):
        super().__init__(parent)      
        self.parent = parent
        self.working = True  # 클래스 내부변수 working을 지정

    def run(self): 
        while self.working:
            for i in range(0, 1000000):     # 스레드 처리를 못해서 "응답없음" 발생
                print(f'출력: {i}')
                # self.pgbTask.setValue(i)
                # self.txbLog.append(f'출력 > {i}')     # 화면을 생성 작동
                self.valChangeSignal.emit(i)            # UI 스레드 화면은 너가 그려줘 
                time.sleep(0.0001) # 1 micro sec 동안 잠재움

            
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
        # Worker 클래스 생성
        self.worker = Worker(self)
        self.worker.valChangeSignal.connect(self.updateProgress) #스레드에서 받은 시그널은
        # updateProgress 함수에서 처리해줌

    
    
    
    @pyqtSlot(int)
    def updateProgress(self, val): # val이 Worker 스레드에서 전달받은 반복값
        self.pgbTask.setValue(val)
        self.txbLog.append(f'출력 > {val}') 
        if val == 999999:
            self.worker.working = False 
        


    # click: 클릴할 때   clicked: 클릭 후 손을 뗐을 때 
    # event = signal (python)
    def btn1_clicked(self):
        self.txbLog.append('실행!!')
        self.pgbTask.setRange(0,999999) 
        self.worker.start()
        self.worker.working = True
      

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qTemplate()
    app.exec_()


