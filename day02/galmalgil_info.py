# 부산 갈맷길 정보 API 크롤링   DB에 저장하자.
import os
import sys
import urllib.request
import datetime
import time
import json
from numpy import result_type
import pandas as pd 
import pymysql #DB에 저장하기 위한 라이브러리임

serviceKey = 'eAVij9xoOwznb%2FOh13NuBhJQ38292SVARj22kJhEDKPXVzYU%2FEfAHLTkBojFja0FcJkzPObXuFiH51V0SlDgfw%3D%3D'


# url 접속 요청 후 응답 리턴 함수
def getRequestUrl(url):
    req = urllib.request.Request(url)

    try: #request가 끊기면 오류가 생겼을 때, 처리하는 방법 정의
        res = urllib.request.urlopen(req)
        if res.getcode() == 200: #200은 ok이고, 400번대는 일반 error, 500번대는 server error
            print(f'[({datetime.datetime.now()})] Url Request success')
            return res.read().decode('utf-8') #에러가 날만한 상황을 제시함
    except Exception as e:
        print(e)
        print(f'[{datetime.datetime.now()}] Error for URL : {url}')
        return None 

def getGalmatgilInfo():
    service_url = 'http://apis.data.go.kr/6260000/fbusangmgcourseinfo/getgmgcourseinfo'   #https --> http 로 변경함.
    params =f'?serviceKey={serviceKey}'#공백안돼
    params += '&numOfRows=10'          ##공백안돼
    params += '&pageNo=1'
    params += '&resultType=json'       #공백안돼
    url = service_url + params

    retData = getRequestUrl(url)



    if retData == None:
        return None
    else:
        return json.loads(retData)


def getGalmalgilService():
    result = [ ] 

    jsonData = getGalmatgilInfo()
    print(jsonData)

    if jsonData['getgmgcourseinfo']['header']['code'] == '00':
        if jsonData['getgmgcourseinfo']['item']== '':
            print("서비스 오류!!")
        else:
            for item in jsonData['getgmgcourseinfo']['item']:
                seq = item['seq']
                course_nm = item['course_nm']
                gugan_nm = item['gugan_nm']
                gm_dgree =  item['gm_degree']
                gm_range = item['gm_range']
                start_pls = item['start_pls']
                start_addr = item['start_addr']
                middle_pls = item['middle_pls']
                middle_adr = item['middle_adr']
                end_pls = item['end_pls']
                end_addr = item['end_addr']
                gm_course = item['gm_course']
                gm_text = item['gm_text']

                result.append([seq,course_nm,gugan_nm,gm_dgree,gm_range,start_pls,  start_addr,  middle_pls, middle_adr,end_pls, end_addr,gm_course, gm_text ])

    return result


def main():
    result = []


    print('부산 갈맷길 코스 조회 합니다.')
    result = getGalmalgilService()
    
    if len(result) > 0:
        #  csv 파일 저장
        columns = ['seq','course_nm','gugan_nm','gm_dgree','gm_range','start_pls',  'start_addr',  'middle_pls', 'middle_adr','end_pls', 'end_addr','gm_course', 'gm_text'] 

        result_df = pd.DataFrame(result, columns = columns)
        result_df.to_csv(f'./부산 갈맷길 코스 조회 합니다.csv', index = False,  encoding='utf-8')
    
        print('csv 파일 저장완료 ! ')


        # DB 저장 - MYSQL PAKAGE 필요함
        connection = pymysql.connect(host = 'localhost', user = 'root', password = 'Park1993!', db = 'crwaling_data')
        cursor = connection.cursor()

        #컬럼명 동적으로 만들기

        cols = '`,`'.join([str(i) for i in result_df.columns.tolist()])

        for i, row in result_df.iterrows():
            sql = 'INSERT INTO `galmatgil_info` (`'+ cols +'` ) VALUES ('+ '%s, '*(len(row)-1) + '%s)' 
            cursor.execute(sql, tuple(row))


        connection.commit()
        connection.close()

        print('DB 저장 완료 ')


if __name__ == '__main__' : 
    main()

    #오픈 preview 로 csv 파일 열어보면 엑셀형식으로 표가 나타난다.