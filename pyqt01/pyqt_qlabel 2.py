#QLabel 일반적인 레이블부터 이미지를 포함한 레이블까지 만들 수 있습니다.

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
        self.setWindowTitle('QLabel')
        self.text = 'What a wonderful world~'
        self.show()


    def addControls(self) -> None:
        self.setWindowIcon(QIcon('./pyqt01/image/lion.png')) #  어플리케이션 윈도우 팝업창의 아이콘 지정

        label1 = QLabel('', self)
        label2 = QLabel('', self)
        label1.setStyleSheet(
            ('border-width: 3px;'                       #박스의 경계선을 나타낸다.
             'border-style: dot-dot-dash;'
             'border-color: blue;'
             'image: url(./pyqt01/image/cute.jpg)')  #박스선 안에 이미지가 나타나게 된다.
            
        )
        

        label2.setStyleSheet(
            ('border-width: 3px;'                       #박스의 점선의 경계선을 나타낸다.
             'border-style: solid;'
             'border-color: red;'
             'image: url(./pyqt01/image/image2.png)')  #박스선 안에 이미지가 나타나게 된다.
            
        )

        # QHBoxLayout()  : 화면에 라벨이 수평으로 두가지 박스 처럼 나온다.
        # QVBoxLayout()  : 화면에 라벨이 수직으로 두가지 박스 처럼 나온다.
        box = QHBoxLayout()                   
        box.addWidget(label1)
        box.addWidget(label2)


        self.setLayout(box)


        # label1.setText('Label1')
        # label2.setText('Label2')
        # self.setLayout(label1)
        # self.setLayout(label2)


    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qTemplate()
    app.exec_()



