##주의 :  Python 3.10.5 로 interpreter로 사용해야한다.

import os 
import sys
import urllib.request
import datetime
import time
import json

client_id = '_P2NqFzoFzwiZAIHlxkJ'
client_secret = 'KStBzX7vGG'


#request : client 가 네이버 서버에  네이버 페이지를 요청한다. 
#response : 네이버 server가 그 요청에  네이버 페이지를 response 해준다. 


# url 접속 요청 후 응답 리턴 함수
def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header('X-Naver-Client-Id', client_id)
    req.add_header('X-Naver-Client-Secret',client_secret)
## 여기까지 url을 불러오는 함수 



# 네이버가 요청에 응답해주면서 그 시간동안에 서버가 연결이 안된다면 try, except 구문으로 해결.
    try:
        res = urllib.request.urlopen(req)
        if res.getcode() == 200: #200은 ok이고, 400번대는 일반 error, 500번대는 server error
            print(f'[({datetime.datetime.now()})] Url Request success')
            return res.read().decode('utf-8')
    except Exception as e:
        print(e)
        print(f'[{datetime.datetime.now()}] Error for URL : {url}')
        return None
# 에러가 뜨면 Error for URL 이라는 문구가 뜨게 한다.



# 핵심함수, 네이버 API 검색
def getNaverSearch(node, srcText, start, display):
    base = 'https://openapi.naver.com/v1/search'
    node = f'/{node}.json'
    text = urllib.parse.quote(srcText) # url 주소에 맞춰서 파싱
    params = f'?query={text}&start={start}&display={display}'

    url = base + node + params
    resDecode = getRequestUrl(url)

    if resDecode==None:
        return None
    else:
        return json.loads(resDecode)
# base페이지에서 node = new로 하고, query 로 text에 우리가 검색할 검색어 +   start page~ display page까지. 나타낸다
# 검색어 :'https://openapi.naver.com/v1/search/news.json?query=코로나 


def getPostData(post, jsonResult, cnt):
    title = post['title']
    description = post['description']
    originallink = post['originallink']
    link = post['link']
    
    pubDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
    pubDate = pubDate.strftime('%Y-%m-%d %H:%M:%S')   # 2022-08-02 15:56:34

    jsonResult.append({'cnt':cnt, 'title': title, 'description': description,
    'originallink': originallink, 'link': link, 'pubDate': pubDate})    


# 실행 최초 함수
def main():
    node = 'news'
    srcText = input('검색어를 입력하세요: ')
    cnt = 0
    jsonResult = []

    jsonRes = getNaverSearch(node, srcText, 1, 50)  

   # print(jsonRes)
    total = jsonRes['total']   #  검색된 뉴스 개수
    
    while ((jsonRes != None) and (jsonRes['display'] != 0)):
        for post in jsonRes['items']:
            cnt += 1
            getPostData(post, jsonResult, cnt)
        
        start = jsonRes['start'] + jsonRes['display']     # 1 +50
        jsonRes = getNaverSearch(node, srcText, start, 50)

    print(f'전체 검색 :{total} 건')

# file output
    with open(f'./{srcText}_naver_{node}.json', mode = 'w', encoding='utf-8') as outfile: 
        jsonFile = json.dumps(jsonResult, indent = 4, sort_keys = True, ensure_ascii= False)
        outfile.write(jsonFile)

    print(f'가져온 데이터 : {cnt}건')
    print(f'{srcText}_naver_{node}.json SAVED')
## 결론 : 스크레핑한 결과 데이터가 JSON파일로 나오게 된다.



# if __name__ =='__main__':"내장변수": 함수의 시작점으로 main 를 실행할거다. 
# "__name__ 이라는 변수의 값이 __main__이라면 다음 코드를 실행하라" 라는 뜻이다
if __name__ =='__main__':
    main()

#해석 : main함수 만들기 : base, node, text, parameter  중에서 main 함수만 메인 페이지로 나오게 할거다. __name___== _main__':뜻.

#print(json)




