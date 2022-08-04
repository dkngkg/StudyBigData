

#할리스 커피숍 매장정보 크롤링
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime

def getHollysStoreInfo(result):

    for page in range(1, 53+1):  #53 page 까지 할리스 홈페이지 수가 있음 
        hollys_url = f'https://www.hollys.co.kr/store/korea/korStore2.do?pageNo={page}'
        #print(hollys_url)
        html= urllib.request.urlopen(hollys_url)
        soup= BeautifulSoup(html, 'html.parser') # 지금까지 전체 html이 다 넘어오게된다.
        tbody = soup.find('tbody')    # html 에서 tbody를 1번만 찾겠다.
       
        for store in tbody.find_all('tr'): # tbody 안의 tr을 전부 다 찾겠다.
            if len(store) <=3:  break      # store 갯수가 3보다 작으면 멈춰라. 하지만 store 개수는 15개 지롱

            store_td = store.find_all('td')
            store_name = store_td[1].string
            store_sido = store_td[0].string
            store_address = store_td[3].string
            store_phone = store_td[5].string

            result.append([store_name]+ [store_sido] + [store_phone ] + [store_address])


def main():
    result =[]
    print('Hollys store crawling >>>')
    getHollysStoreInfo(result)


  # 판다스 데이터 프레임 생성
    columns = ['store', 'sido-gu', 'address', 'phone']
    hollys_df= pd.DataFrame(result, columns=columns)

    # csv 저장
    #hollys_df.to_csv('C:/localRepository/StudyBigData/day03/hollys_shop_info.csv',index = True, encoding = 'utf-8')
    hollys_df.to_csv('./hollys_shop_info2.csv',index = True, encoding = 'utf-8')
    print('저장완료')

    del result[:]


if __name__ == '__main__':
    main()


                









