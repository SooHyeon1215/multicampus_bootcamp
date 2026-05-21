import pandas as pd
import time
from datetime import datetime


#code_list의 종목 코드의 값들을 유저가 입력한 값들로 채운다.
code_list=[]

#반복문을 생성을 하는데 반복횟수는 명확하지 않다 
while True:
    #유저가 데이터를 입력한다.
    input_code=input('종목 코드를 입력하시오 (입력값 종료 시 ENTER)')
    #종목 코드는 길이가 6
    if len(input_code)==6:
        code_list.append(input_code)
    
    #input_code가 존재하지 않는다면 
    if not(bool(input_code)):
        break

now=datetime.now()
now_str=now.strftime('%Y-%m-%d')

for code in code_list:
    # print(code)
    #주소를 반복 실행할떄마다 변경
    base_url='https://comp.wisereport.co.kr/company/c1010001.aspx?cmp_cd='

    # print(base_url + code)
    #read_html을 이용해서 table데이터를 크롤링 -> 4번째 표를 선택
    df=pd.read_html(base_url + code)[3]
    
    #데이터프레임을 csv파일로 저장(파일의 이름은 종목코드.csv)
    #데이터프레임 타입에서 csv 타입으로 변경 -> 타입이 변경될때 사용하는 주요 키워드(to)
    #같은 파일에 새로운 데이터가 입혀지는 형태
    #날찌별로 실행할때마다 새로운 파일이 생성(현재 시간을 로드 파일명으로 사용)
    df.to_csv(f'./{code} {now_str}.csv')
    
    #시간의 딜레이 생성
    time.sleep(1)