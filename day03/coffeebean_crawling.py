# Selenium 사용 웹페이지 크롤링

# 패키지로드
## < Selenium 패키지 추가 ###>
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver


def getCoffeeBeanStoreInfo(result):
    #chrome webdriver 객체 생성
    #커피빈 사이트 ! 
    wd = webdriver.Chrome('./day03/chromedriver.exe')   #경로 주의!!!!
    
    for i in range(1,11):
        wd.get('https://www.coffeebeankorea.com/store/store.asp')
        time.sleep(1)

        try:
            wd.execute_script(f"storePop2('{i}')")
            time.sleep(1)   #팝업표시 후에 크롤링이 안되서 브라우저가 닫히는 것을 방지
            html = wd.page_source
            soup = BeautifulSoup(html,'html.parser')
            store_name = soup.select('div.store_txt > h2')[0].string
            print(store_name)
            store_info = soup.select('table.store_table > tbody> tr > td')
            store_address_list = list(store_info[2])
            store_address = store_address_list[0].strip()
            store_contact = store_info[3].string
            result.append([store_name]+ [store_contact] +[store_address])

        except Exception as e:
            print(e)
            continue


def main():
    result = []
    print('커피빈 매장 크롤링 >>> ')
    getCoffeeBeanStoreInfo(result)

if __name__ == '__main__':
         main()














