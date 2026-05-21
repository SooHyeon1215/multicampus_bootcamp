class Bank():

    #class 변수를 생성(같은 class를 생성하는 객체들끼리 서로 공유할 수 있는 변수)
    total_cost=0    #모든 유저가 입금/츨금시 total_cost의 변화(class 생성 시 _cost를 total_cost에 누적합)
    user_cnt=0      #class 생성 시 1싹 증가
    # user_list=[]
    #생성자 함수 : 매개변수 4개
    # def __init__(self, _name, _birth, _cost=0, _log=[]):
    def __init__(self, _name, _birth, _cost=0):
        self.name=_name
        self.birth=_birth
        self.cost=_cost
        # self.log=_log
        self.log=[]
        #class 변수에 접근하는 방법
        Bank.total_cost +=_cost
        Bank.user_cnt+=1
        # self.user_list=Bank.user_list --> 쓰레기 코드 (필요 없는 코드)

    #입금 함수
    def add_cost(self,_c):
        #단순하게 self.cost를 _c만큼 증가
        self.cost+=_c
        # self.cost=self.cost+_c
        #로그 내역 추가
        dict_data={
            'type' : '입금',
            'cost' : _c, 
            'total_cost' :self.cost}
        #class 변수 은행의 총 잔액을 증가
        Bank.total_cost+=_c
        self.log.append(dict_data)
        print(f'입금이 완료 되었습니다. 현재의 잔액은 {self.cost}입니다.')
    #출금 함수
    def sub_cost(self,_c):
        #현재의 잔액보다 _c가 큰 경우
        if self.cost<=_c:
            
            self.cost-=_c
            dict_data={
                'type' : '출금',
                'cost' : _c,
                'total_cost' :self.cost
            }
            #거래내역을 추가
            self.log.append(dict_data)
            #class 뱐수 은행 총 잔액을 감소
            Bank.total_cost-=_c
            print(f'출금이 완료되었습니다. 현재의 잔액은 {self.cost}입니다.')
            #츨금이 정상적으로 작동했을 때 1을 되돌려준다.
            return 1
        else:
            #출금이 불가능한 상황
            #self.cost 유지 --> 아무 헹동도 하지 않는다.
            print('현재 잔액이 부족합니다.')
            #출금 실패 시 0을 되돌려준다.
            return 0
    #user_info() 함수를 생성하여 이름과 생년월일, 현재 잔액을 출력하는 함수
    def user_info(self):
        print(f'이름 : {self.name}, 생년월일 : {self.birth}, 잔액 : {self.cost}')

from typing import override
#일의 종류 
#   -> 함수 안에서 여러 조건식을 이용하여 일의 종류, 시급들을 지정 
#   -> DatBase(데이터들을 모아두는 공간)를 이용하여 데이터를 로드
#   -> key : value의 형태를 이용하여 일의 종류 : 시급 이라는 형태의 데이터를 사용
#구매할 수 있는 물품 리스트
#   -> dict 형태의 key : value의 형태를 이용하여 지정이 가능
#   -> 함수 안에서 여러 조건식 사용 가능
#   -> DB 안에 데이터를 이용하여 사용 가능

#두개의 데이터셋은 dict 형태로 class 변수로 지정
# (같은 class를 생성했을대 일의 종류와 물건의 종류는 서로 공유가 가능하게 하기 위해)

class User(Bank):

    #일의 종류와 시급 dict 데이터를 class 변수로 생성
    work_type={
        'A':11000,
        'B':15000,
        'C':20000
    }
    #구매하고 싶은 물건
    item_list={
        '텀블러':50000,
        '스위치':730000,
        '태블릿 거치대':20000,
        '헤드셋':520000,
        '노트북':2000000
    }

    #생성자 함수
    def __init__(self,_name,_birth,_cost):
        #_name,_birth,_cost는 부모 클래스의 생성자 함수를 호출해서 인자로 사용
        super().__init__(_name,_birth,_cost)
        #super().__init__() -> 생성이 되는 변수의 개수는?
        #구매한 아이템의 목록 -> 빈 리스트로 생성
        self.items=[]

    #일을 한다... 함수(매개변수 : 일의 종류, 시간)
    def work(self,_type,_time):
        #_type이 work_types에 데이터기 존재하는가?
        #dict 데이터에서 key 값들 중에 _type의 값이 포함되어 있는가?
        #in 비교 연산자 -> 단일 데이터 in 1차원 데이터 -> 1차원 데이터 원소 중 단일 데이터가 포함되어있는가?
        if _type in User.work_type:
            #일의 종류 데이터에 _type이 포함되어 있는 경우
            #시급 데이터를 로드하고 _time과 * 연산을 한다.
            #시급 -> work_type 데이터가 존재
                #{'A':11000, 'B':15000, 'C':20000} <- User.work_type
            #_type이 'A'라고 입력값이 들어왔다면 : User.work_type['A'] ->11000 --> 'A'라는 일의 시급
            #시급*시감 --> 일당
            #일당을 통장에 입금
            amount=User.work_type[_type]*_time #일당을 계산
            # print(User.work_type)
            # print(User.work_type[_type]) #시급
            # print(amount)       #일당을 출력
            #일당이 계산되었으니 일당을 통장(Bank : 부모클레스 ->super())에(~안에) 입금(add_cost(금액))
            super().add_cost(amount) #->add_cost라는 함수는 입금완료 출력이 존재
        else:
            #일의 타입이 맞지 않는 경우
            # print('일의 타입이 맞지 않습니다.')
            #잘못된 데이터가 들어왔을 때 에러 발생 raise
            #TypeError : 데이터의 타입이 맞지 않는다.
            #ValueError : 데이터의 값이 잘못되었다.
            raise ValueError('저장되어 있는 일의 종류가 아닙니다.')
    #물건을 구매하자(스트레스 해소) -> 매개변수 1개(믈건의 종류)
    def buy_item(self,_item):
        #wok() 함수에서는 일의 종류가 포함되어 있는가? -> in이라는 비교연산자 사용

        #try ~ except : 코드를 실행하는데 예외가 발생했을때 특정한 행동을 할때 사용
        try:
            #시도할 코드
            #물건의 가격을 로드
            #물건의 가격은 User 클래스 안에 item_list에 dict 형태로 존재 -> key를 이용해서 가격을 추출 dict[key]
            #key로 사용될 데이터는 _item
            # print(User.item_list)
            # print(User.item_list[_item])    #물건의 가격을 추출
            #가격을 알았으니 출금(Bank(super()) 안에 sub_cost(금액))
            #잔액이 부족하면 0을 되돌려주고, 정상적으로 출금이 되면 1을 되돌려준다.
            sub_res=super().sub_cost(User.item_list[_item])
            #sub_res가 1이면 구매 성공 -> items에 구매한 물건을 추가
            # if sub_res == 1:
            if sub_res:
                #구매 성공
                self.items.append(_item)
                print('구매 성공')
            else:
                #구매 목록에 추가하지 않는다. -> 아무 행동도 하지 않는다.
                print('구매 실패')
        except Exception as e:
            #Exception : 에러의 메시지
            #as : 별칭을 짓갰다.
            #e : 별칭 명
            #에러의 종류 출력
            print(type(e).__name__)
            print(e) #어떤 에러가 발생했는지 이유를 print()로 출력
            #try 영역에서 실행되는 코드가 예외가 발생했을때만 실행이 되는 영역
            print('물건의 정보가 없습니다.')
    #오버라이드 : 부모 클래스의 기능의 이름을 덮어씌워서 사용
    #(부모 클래스에서는 1이라는 기능, 자식 클래스에서는 2라는 기능) -> 부모 클레스의 함수의 기능은 그대로 유지
    #이름, 생년월일, 잔액, 구매한 물건의 목록을 출력
    @override       #'문법적으로 오버라이드 함수입니다'를 가독성이 좋게 표시 ()
    def user_info(self):
        print(f'이름 :{self.name}, 생년월일 : {self.birth}, 잔액 : {self.cost}, 구매한 물건의 목록 :{self.items}')
        #User 클래스에서는 이름 생년월일 잔액 물건의 목록을 출력
        #Bank 클래스에서는 이름 생년월일 잔액을 출력
        


#모듈은 변수, 함수, 클래스의 모음 => py 파일로 생성
test_vari = '모듈 안의 변수 데이터'

def func_1(a,b):
    return a+b
