#QFont 가장 기본이 되는 템플릿 소스입니다.

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt

# 클래스 OOP
class qTemplate(QWidget):
    # 생성자
    def __init__(self) -> None:      #class 이므로 self : qtpy 본인을 뜻한다. 함수 후 return을 해야하는데, 이 경우 '생성자'이므로 None: return 값이 없다.
        super().__init__()
        self.initUI()

# 화면 정의를 위해 사용자 함수
    def initUI(self) -> None:
        self.setGeometry(300, 100, 640, 400)     
        self.setWindowTitle('QTemplate!! welcome')
        self.text = 'What a wonderful world~'
        self.show()

    # 텍스트 그리기 위한 사용자 함수
    def paintEvent(self, event) -> None:     # 그림 그릴 수 있게 하는 함수임. 
        paint = QPainter()
        paint.begin(self)
        # 그리는 함수 추가
        self.drawText(event, paint)         # 글자를 심어 넣은 거임
        paint.end()

    def drawText(self, event, paint):
        paint.setPen(QColor(50,50,50))
        paint.setFont(QFont('NanumGothic', 20))
        paint.drawText(105, 100, 'HELL WORLD~')

        paint.setPen(QColor(0,255,10))
        paint.setFont(QFont('Impact', 14))
        paint.drawText(event.rect(), Qt.AlignCenter, self.text)







if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qTemplate()
    app.exec_()



