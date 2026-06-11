import pandas as pd
import numpy as np
from konlpy.tag import Okt
from gensim.models import FastText
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import os

# 1. 데이터 로드
file_path = r'c:\Users\user\OneDrive\문서\GitHub\multicampus_bootcamp\260609\ratings_test.txt'
if not os.path.exists(file_path):
    print("파일을 찾을 수 없습니다. 경로를 확인해주세요.")
else:
    df = pd.read_csv(file_path, sep='\t')
    # 결측치 제거 (리뷰 내용이 없는 행 처리)
    df = df.dropna(subset=['document'])

    # 2. 형태소 분석 및 토큰화 (Okt 사용)
    okt = Okt()
    print("데이터 토큰화 중...")
    # 모든 문장을 형태소 단위로 나누고 스테밍(어간 추출) 처리
    tokenized_docs = [okt.morphs(doc, stem=True) for doc in df['document']]

    # 3. FastText 임베딩 모델 학습
    print("FastText 임베딩 학습 중...")
    # vector_size: 임베딩 차원, window: 주변 단어 범위, min_count: 최소 출현 빈도, sg: 1(Skip-gram)
    ft_model = FastText(sentences=tokenized_docs, 
                        vector_size=100, 
                        window=5, 
                        min_count=2,
                        workers=4, 
                        sg=1)

    # 4. 문서 벡터 생성 함수 (단어 벡터들의 평균값 사용)
    def get_document_vector(tokens, model):
        # 모델의 단어장에 존재하는 단어들만 벡터 추출
        vectors = [model.wv[word] for word in tokens if word in model.wv]
        if not vectors:
            return np.zeros(model.vector_size)
        return np.mean(vectors, axis=0)

    print("문서 벡터화 중...")
    X = np.array([get_document_vector(tokens, ft_model) for tokens in tokenized_docs])
    y = df['label'].values

    # 5. 데이터 분할 (학습용 80%, 테스트용 20%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 6. SVC 모델 생성 및 학습
    print("SVC 모델 학습 중 (데이터 양에 따라 시간이 소요될 수 있습니다)...")
    # kernel='rbf'는 비선형 분류에 효과적입니다.
    svc = SVC(kernel='rbf', C=1.0, gamma='scale')
    svc.fit(X_train, y_train)

    # 7. 예측 및 결과 출력
    y_pred = svc.predict(X_test)
    
    print("\n[학습 결과]")
    print(f"정확도(Accuracy): {accuracy_score(y_test, y_pred):.4f}")
    print("\n[상세 보고서]")
    print(classification_report(y_test, y_pred))

    # 예시 문장 테스트
    test_sentence = "진짜 시간 가는 줄 모르고 봤어요. 추천합니다!"
    test_tokens = okt.morphs(test_sentence, stem=True)
    test_vec = get_document_vector(test_tokens, ft_model).reshape(1, -1)
    result = svc.predict(test_vec)
    print(f"\n테스트 문장: '{test_sentence}'")
    print(f"예측 결과: {'긍정(1)' if result[0] == 1 else '부정(0)'}")
