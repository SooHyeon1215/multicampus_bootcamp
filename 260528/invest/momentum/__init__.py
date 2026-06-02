import pandas as pd
import numpy as np
from datetime import datetime


def create_ym(_df, _col='Adj Close'):
    df=_df.copy()
    #Date가 컬럼에 포함되어 있는가?
    if 'Date' in df.columns:
        df.set_index('Date', inplace=True)
    df.index=pd.to_datetime(df.index)
    df.index=df.index.tz_localize(None)
    #결측치, 무한대 데이터 제거
    flag=df.isin([np.nan, np.inf, -np.inf]).any(axis=1)
    df=df.loc[~flag, [_col]]
    #파생 변수 STD-YM
    df['STD-YM']=df.index.strftime('%Y-%m')

    return df


def create_month(
    _df,
    _start='2010-01-01',
    _end=datetime.now(),
    _momentum=12,
    _last=1
):
    #_last 값에 따라서 월말, 월초
    if _last == 1:
        df = _df.groupby('STD-YM').tail(1)
    elif _last == 0:
        df = _df.groupby('STD-YM').head(1)
    else:
        return '_last의 값은 0과 1만 가능합니다.'
    #기준이 되는 컬럼의 이름을 변수로 저장
    col=_df.columns[0]
    #전월의 데이터를 BF1에 대입
    df['BF1']=df.shift(1)[col].fillna(0)
    df['BF2']=df.shift(_momentum)[col].fillna(0)

    #시작시간과 종료시간을 기준으로 데이터를 필터링
    df=df.loc[_start : _end,]
    return df


def create_trade_rtn(_df1,_df2, _score=1):
    df=_df1.copy()

    df['trade']=''
    df['rtn']=1
    col=df.columns[0]

    #_df2를 이용해서 거래내역을 생성
    for i in _df2.index:
        signal=''
        #모멘텀 계산
        momentum_index=_df2.loc[i,'BF1']/_df2.loc[i,'BF2']-_score
        flag=(momentum_index > 0) & (momentum_index != np.inf)
        if flag:
            signal ='buy'

        #거래 내역 생성
        df.loc[i:, 'trade']=signal
        print(f'날짜 : {i}, 모멘텀 인덱스 : {momentum_index}, signal : {signal}')
    
    #수익율 계산
    for i in df.index:
        if (df.shift().loc[i,'trade'] == '') & (df.loc[i,'trade'] == 'buy'):
            buy=df.loc[i,col]
            print(f'매수일 : {i}, 매수가 : {buy}')
        elif (df.shift().loc[i,'trade'] == 'buy') & (df.loc[i,'trade'] == ''):
            sell = df.loc[i,col]
            rtn=sell/buy
            df.loc[i,'rtn']=rtn
            print(f'매도일 : {i}, 매도가 : {buy}, 수익율 : {rtn}')

    #누적 수익율 계산
    df['acc_rtn']=df['rtn'].cumprod()

    acc_rtn=df.iloc[-1,-1]

    return df, acc_rtn