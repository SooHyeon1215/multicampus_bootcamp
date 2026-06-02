import numpy as np 
from datetime import datetime
import pandas as pd 

# create_band(), create_trade(), create_rtn() 함수를 복사 붙여넣기 


def create_band(
        _df, 
        _col = 'Adj Close', 
        _start = '2010-01-01', 
        _end = datetime.now(), 
        _cnt = 20
):
    # 복사본 생성 : 깊은 복사 
    df = _df.copy()
    # 인덱스가 Date인가? -> 컬럼중에 Date가 존재하는가?
    if 'Date' in df.columns:
        # 포함되어있다면? -> Date를 index로 변경
        df.set_index('Date', inplace=True)
    # index를 시계열로 변경 
    df.index = pd.to_datetime(df.index)
    # timezone 제거 
    df.index = df.index.tz_localize(None)
    # 결측치, 무한대 데이터를 제거 
    flag = df.isin([np.nan, np.inf, -np.inf]).any(axis=1)
    df = df.loc[~flag, ]
    # 기준이 되는 컬럼을 제외하고 모두 제거 
    df = df[[_col]]
    # 이동평균선, 상단밴드, 하단밴드 생성
    df['center'] = df[_col].rolling(_cnt).mean()
    std_value = 2 * df[_col].rolling(_cnt).std()
    df['ub'] = df['center'] + std_value
    df['lb'] = df['center'] - std_value
    # 시작 시간과 종료시간으로 필터링 
    df = df.loc[_start:_end, ]
    return df

def create_trade(_df):
    # 기준이 되는 컬럼의 이름을 어떻게 알것인가? -> 첫함수의 결과값을 생각. -> columns => ['Adj Close', 'center', 'ub', 'lb']
    # 기준이 되는 컬럼은 _df에서 첫번쨰 컬럼의 이름이구나 .
    col = _df.columns[0]

    df = _df.copy()

    df['trade'] = ''

    for i in df.index:
        if df.loc[i, col] >= df.loc[i, 'ub']:
            # 매도 
            df.loc[i, 'trade'] = ''
        elif df.loc[i, col] <= df.loc[i, 'lb']:
            # 매수
            df.loc[i, 'trade'] = 'buy'
        else:
            if df.shift().loc[i, 'trade'] == 'buy':
                df.loc[i, 'trade'] = 'buy'
            else:
                df.loc[i, 'trade'] = ''
    return df

def create_rtn(_df):
    col = _df.columns[0]
    df = _df.copy()

    df['rtn'] = 1

    # 수익율 계산
    for i in df.index:
        # 매수 
        if (df.shift().loc[i, 'trade'] == "") & (df.loc[i, 'trade'] == "buy"):
            buy = df.loc[i, col]
            print(f"매수일 : {i}, 매수가 : {buy}")
        elif (df.shift().loc[i, 'trade'] == "buy") & (df.loc[i, 'trade'] == '') :
            sell = df.loc[i, col]
            rtn  = sell / buy
            df.loc[i, 'rtn'] = rtn

            print(f"매도일 : {i}, 매도가 : {sell}, 수익율 : {rtn}")
    # 누적 수익율 계산
    df['acc_rtn'] = df['rtn'].cumprod()
    # 최종 수익율
    acc_rtn = df.iloc[-1, -1]

    return df, acc_rtn