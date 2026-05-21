import pandas as pd
import os

def data_load(file_path,
              file_ext = 'csv',
              output_type = 'concat',
              engine ='utf-8'):
    #파일 path에 '/' 추가
    file_path+='/'
    file_list=os.listdir(file_path)
    #파일 목록이 file_ext와 ekfms 확장자가 포함되어있을 수 있다.
    #필터 -> 마지막이 file_ext와 같다면 리스트에 유지, 아니면 제거
    #case1
    file_list2=[x for x in file_list if x.endswith(file_ext)]
    # #case2
    # file_list2=[]
    # for x in file_list:
    #     if x.endswith(file_ext):
    #         #확장자가 csv와 같은 경우
    #         file_list2.append(x)

    #output_type이 concat이라면 빈 데이터프레임을 생성
    if output_type =='concat':
        result=pd.DataFrame()
    elif output_type =='global':
        #전역변수에서 사용할 넘버 생성
        vari_cnt=1
    else:
        #concat, global 이 아니라면 -> 에러발생 ValueError
        raise ValueError('output_type에는 concat이나 global만 사용이 가능합니다.')
        #에러기 발생 -> 함수도 종료

    #파일을 로드
    for file_name in file_list2:
        #file_ext에 따라 read_xxx() 선택
        if file_ext =='csv':
            df=pd.read_csv(file_path + file_name, encoding=engine)
        elif file_ext =='json':
            df=pd.read_json(file_path + file_name, encoding=engine)
        elif file_ext == 'xml':
            df=pd.read_xml(file_path + file_name, encoding=engine)
        # elif (file_ext == 'xlsx') or (file_ext=='xls') :
        elif file_ext in ['xlsx','xls']:
            #read_excel() 함수는 encoding 매개변수 존재하지 않는다.
            df=pd.read_excel(file_path + file_name)
        else:
            #위믜 모든 조건이 거짓인 경우 -> ValueError
            raise ValueError('file_ext에는 csv,json,xml,excel 확장자만 선택이 가능합니다.')
        
        #output_type에 따라 결합, 전역변수 저장
        if output_type == 'concat':
            result=pd.concat([result, df])
        else:
            #전역변수에 저장
            globals()[f'df_{vari_cnt}']=df.copy()
            print(f'df_{vari_cnt} 전역 변수가 생성')
            #vari_cnt 1씩 증가
            vari_cnt+=1
            
    #결과를 되돌려준다.
    try:
        #코드를 실행한다
        return result
    except:
        #try 코드가 실패하면 실행
        print('전역변수 생성 완료')