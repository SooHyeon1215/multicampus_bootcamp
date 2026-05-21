import numpy as np
# 수정작업1차(20260507) : 2번째 매개변수 컬럼 값을 가변 인자로 변경 (col -> cols 변경)
# def outlier_iqr(data, col, n = 1.5, drop = False):
def outlier_iqr(data, *cols, n = 1.5, drop = False):
    # 원본의 데이터를 그대로 유지하기 위해서 복사 
    df = data.copy()
    # 입력으로 받은 데이터프레임 안에 col의 값이 컬럼으로 존재하는가? -> 해당 컬럼의 데이터 타입이 숫자인가?
    # if col in df.columns:
    # 우선 실행한다 에러가 발생하면 예외 처리 한다. try ~ except
    # 수정작업1차 안 cols를 사용하면 반복문 추가 
    # 경계에서 벗어난 데이터프레임들을 dict 형태로 되돌려준다. {col : DataFrame, dol2 : DataFrame}
    whis_dict = {}
    for col in cols:
        try:
            # 1,3 사분위수를 계산
            q_1, q_3 = np.percentile(df[col], [25, 75])
            iqr = q_3 - q_1

            # 상단의 경계, 하단의 경계 값 계산
            upper_whis = q_3 + ( n * iqr )
            lower_whis = q_1 - ( n * iqr )
            # 경계값들 출력 
            print( f"""
                지정된 컬럼의 이름 : {col}, 
                상단의 경계 값 : {upper_whis}, 
                하단의 경계 값 : {lower_whis}
            """ )
            # 상단의 경계를 벗어나는 데이터의 개수 확인 
            upper_flag = df[col] > upper_whis
            lower_flag = df[col] < lower_whis
            upper_n = len( df.loc[upper_flag, ] )
            lower_n = len( df.loc[lower_flag, ] )
            print(f" 상단의 경계를 벗어나는 데이터의 개수 : {upper_n} 하단의 경계를 벗어나는 데이터의 개수 : {lower_n} ")
            # 극단치 경계에서 벗어난 데이터들
            whis_df = df.loc[ upper_flag | lower_flag,  ]
            # whis_df를 whis_dict에 추가 
            whis_dict[col] = whis_df
            if drop:
                # 극단치들을 제거 
                df = df.loc[ ~( upper_flag | lower_flag ), ]
            else:
                df.loc[upper_flag, col] = upper_whis
                df.loc[lower_flag, col] = lower_whis
            
            # 결과물, 극단치의 경계에서 벗어난 데이터들을 되돌려준다. 
            # return df, whis_df

        except Exception as e:
            print(f"Error : {e}")
    return df, whis_dict