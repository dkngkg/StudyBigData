## 0818 은 어제 navernews.ui에서 여러 버튼이 추가됨. '데이터', '저장할 데이터'    

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import *

from urllib.parse import quote
import urllib.request
import json
import webbrowser
import pandas as pd # csv 저장용

# UI 스레드와 작업스레드 분리
class Worker(QThread):
        #QTread는 UI를 그릴 권한이없다
        valChangeSignal = pyqtSignal(int)
        def __init__(self,parent) -> None:
            super().__init__(parent)
            self.parent = parent
            self.working = True # 클래스 내부변수 working을 지정

        def run(self):
            while self.working:
                for i in range(0, 100):
                    print(f'출력 : {i}')
                    # self.pgbTask.setValue(i)
                    # self.txblog.append(f'출력>{i}') # 화면 그리는 작업
                    self.valChangeSignal.emit(i) # UI스레트야 화면은 너가 그려줘~
                    time.sleep(0.0001) # 1micro sec



# 클래스 OOP
class qTemplate(QWidget):
    # 생성자, 생성자는 기본적으로 return값이 없다. 그래서 None
    # 대신 통신을 통해서 UI스레드가 그림을 그릴 수있도록 통신수행
    # 생성자, 생성자는 기본적으로 return값이 없다. 그래서 None

    start = 1 # api 호출할 때 시작하는 데이터 번호
    max_display = 100 # 한페이지에 나올 데이터 수 
    saveResult = [] # 저장할 때 담을 데이터(딕셔너리 리스트) - > DataFrame이 된다.
    


    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('./pyqt03/navernews_2.ui',self)    # 화면 UI 변경
        self.initUI()
    
    def initUI(self) -> None:
        self.addControls()
        self.show()

    def addControls(self) -> None: # 위젯 정의, 이벤트(시그널)처리
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        self.txtSearch.returnPressed.connect(self.btnSearchClicked)   #편의성!! -  '손흥민' 검색하고 enter 누르면 다 자동으로 검색된다! !! 굳이 검색 버튼을 누르지 않아도 된다.ss
        self.tblResult.itemSelectionChanged.connect(self.tblResultSelected)
        # 22.08.18 추가 버튼 이벤트(시그널) 확장 
        self.btnNext.clicked.connect(self.btnNextClicked) 
        self.btnSave.clicked.connect(self.btnSaveClicked)

    def btnNextClicked(self) -> None: 
        self.start = self.start + self.max_display
        self.btnSearchClicked()

    def btnSaveClicked(self) -> None: 
        if len(self.saveResult) > 0 :
            df = pd.DataFrame(self.saveResult)
            df.to_csv(f'./pyqt03/{self.txtSearch.text()}_뉴스검색결과.csv', encoding='utf-8', index = True)
        
        QMessageBox.information(self, '저장', '저장완료!')
        #저장 후 모든 변수 초기화
        self.saveResult = []
        self.start = 1
        self.txtSearch.setText('')
        self.lblStatus.setText('Data: ')
        self.lblStatus2.setText('저장할 데이터 > 0개')
        self.tblResult.setRowCount(0)
        self.btnNext.setEnabled(True)




    def tblResultSelected(self) -> None:
        selected = self.tblResult.currentRow() # 현재 선택된 열의 인덱스
        link = self.tblResult.item(selected, 1).text()
        webbrowser.open(link)

    def btnSearchClicked(self) -> None: # 슬롯(이벤트핸들러)
        jsonResult = []
        totalResult = []
        keyword = 'news'
        search_word = self.txtSearch.text()
      
        # QMessageBox.information(self, '결과',search_word)
        jsonResult = self.getNaverSearch(keyword, search_word, self.start, self.max_display)
        
        for post in jsonResult['items']: #구성요소중 ['items']를 선택해서 items에서 하위내용 찾는 것
            totalResult.append(self.getPostData(post))
            
        # print(totalResult)
        self.makeTable(totalResult)
        # return뒤에 아무 값이 없으면 none값이다

        # saveResult 값 할당, lblStatus /2 상태값을 표시
        total = jsonResult['total']
        curr = self.start + self.max_display - 1

        self.lblStatus.setText(f'Data : {curr} / {total}')

        # saveResult 변수에 저장할 데이터를 복사
        for post in totalResult:
            self.saveResult.append(post[0])

        self.lblStatus2.setText(f'저장할데이터 > {len(self.saveResult)}개')  # "저장할데이터" 문구가 뜸.  
        


        if curr >= 1000:
            self.btnNext.setDisabled(True) # 다음버튼 비활성화  #1000건 이상부터 다음버튼 안눌러지게 함.

        else:
            self.btnNext.setEnabled(True) # 활성화



    def makeTable(self, result):
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tblResult.setColumnCount(2)
        self.tblResult.setRowCount(len(result)) # displayCount에 따라서 변경,현재는 50
        self.tblResult.setHorizontalHeaderLabels(['기사제목','뉴스링크'])
        self.tblResult.setColumnWidth(0, 350)
        self.tblResult.setColumnWidth(1, 100)
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers) #readonly

        i=0
        for item in result:
            title = self.strip_tag(item[0]['title'])
            link = item[0]['originallink']
            self.tblResult.setItem(i, 0, QTableWidgetItem(title))
            self.tblResult.setItem(i, 1, QTableWidgetItem(link))
            i+=1


    def strip_tag(self, title):  # html tag 없애주는 함수
        ret = title.replace('&lt;', '<')
        ret = ret.replace('&gt;', '>')
        ret = ret.replace('&quot;', '"')
        ret = ret.replace('&apos;', "'")
        ret = ret.replace('&amp;', '&')
        ret = ret.replace('<b>', '')
        ret = ret.replace('</b>', '')
        return ret
        






    def getPostData(self,post): #내가 원하는 데이터를 뽑기 위해서 하위의 json코드를 선택하는 것
        temp = []
        title = self.strip_tag(post['title'])   # 모든 곳에서 html 태그 제거
        description = post['description']
        originallink = post['originallink']
        link = post['link']
        pubDate = post['pubDate']

        temp.append({'title':title,
                    'description':description,
                    'originallink':originallink,
                    'link':link,
                    'pubDate': pubDate})  #220818 pubDate 빠진거 추가

        return temp


    # 네이버 API크롤링을 위한 메인 함수
    def getNaverSearch(self, keyword, search, start, display):
        url = f'https://openapi.naver.com/v1/search/{keyword}.json'\
              f'?query={quote(search)}&start={start}&display={display}'#quote는 한글을 urlloard하기위한 함수
        print(url)

        req = urllib.request.Request(url)
        # 네이버 인증추가
        req.add_header('X-Naver-Client-Id','SH3HwdwkmEE_HUKzTyxW')
        req.add_header('X-Naver-Client-Secret','QOikKo2ZEW')

        res = urllib.request.urlopen(req)
        if res.getcode() == 200:
            print('URL request success')
        else:
            print('URL request failed')

        ret = res.read().decode('utf-8')
        if ret == None:
            return None
        else:
            return json.loads(ret)




if __name__=='__main__':
    app = QApplication(sys.argv)
    ins = qTemplate()
    app.exec_()
