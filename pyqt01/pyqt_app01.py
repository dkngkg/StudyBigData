# 가장 심플한 PyQt 실행방법

from PyQt5 import QtWidgets as qw

def run():
  app = qw.QApplication([])    # widget이란 것이 뜬다
  wnd = qw.QMainWindow()       # 팝업으로 띄우는 창
  lab = qw.QLabel('hello Qt!') # 창 안에 나오는 문당
  wnd.setCentralWidget(lab)
  wnd.show()
  app.exec_()


if __name__ == '__main__':
  run()