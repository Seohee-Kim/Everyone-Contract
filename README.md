# Everyone's Contract with KoBERT 
* 중고거래 리카르디안 계약서 생성
* KoBERT를 활용한 채팅 내 핵심어 자동추출 모델 및 테스트 페이지 구성  
* Overview(예정)  
<img> </br></br>

## Summary  
* 👩‍💻 **기여** : 모델링 아이디어 설계 및 모델링 (2명)
  
* 👩‍💻 **역할** : AI Engineer
  
* 👩‍💻 **기간** : 약 3주
	* 리서치 (2021.07.07 ~ 07.13)
  * 모델링 (2021.07.19 ~ 07.26)
  * 1차 발표 및 피드백 (2021.08.05 ~ 08.12)
  * 장고 페이지 제작 (2021.08.18 ~ 2021.08.28)
  * 보완 (2021.09.15 ~ 09.22) 
  * 2차 발표 및 피드백 (2021.10.05 ~ 10.15) </br></br>

## 작업환경
* **💻 학습** : AWS EC2, Colab, Atom
  
* **💻 코드** :  [모델링](https://github.com/Seohee-Kim/KoBERT-EveryoneContract/blob/main/Everyones_Contract_Classifier(v4).ipynb), [함수](https://github.com/Seohee-Kim/KoBERT-EveryoneContract/tree/main/pages/KobertModule)
  
* **💻 발표자료**  : [1차 발표](https://github.com/Seohee-Kim/KoBERT-EveryoneContract/blob/main/KoBERT%201%E1%84%8E%E1%85%A1%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%20%E1%84%87%E1%85%A9%E1%84%80%E1%85%A9.pdf), [2차 발표](https://github.com/Seohee-Kim/KoBERT-EveryoneContract/blob/main/KoBERT%202%E1%84%8E%E1%85%A1%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%20%E1%84%87%E1%85%A9%E1%84%80%E1%85%A9%20(%E1%84%8C%E1%85%A1%E1%86%BC%E1%84%80%E1%85%A9%20%E1%84%91%E1%85%A6%E1%84%8B%E1%85%B5%E1%84%8C%E1%85%B5%20%E1%84%80%E1%85%AE%E1%84%89%E1%85%A5%E1%86%BC%20%E1%84%86%E1%85%B5%E1%86%BE%20%E1%84%89%E1%85%A1%E1%84%8B%E1%85%AD%E1%86%BC%E1%84%87%E1%85%A1%E1%86%BC%E1%84%87%E1%85%A5%E1%86%B8)%20.pdf) </br></br>

## 스프린트
* [Problem & Solving](https://docs.google.com/document/d/15GPdiYNVQkrFdvSEoxeyJj5ED2m2assSFfMkXpnDg0w/edit?usp=sharing)

  |                           Problem                            |                           Solving                            |
  | :----------------------------------------------------------: | :----------------------------------------------------------: |
  | **OCR 변환 방식**<br />전체 문장을 입력값으로 사용 (추출 정확도 낮음) | **턴(turn) 단위 분리 저장**<br /> 핵심어 포함 문장의 라벨 배정 확률 높임 |
  | **정규표현식 제한적**<br />한국어에 맞지 않는 설계, 구어 및 약어 비인식 | **정규표현식 개선**<br />경우의 수 추가, 상대적 날짜 인식 개선 |
  |     **NNG "매핑" 인식** <br /> 딕셔너리 구성에 추가 공수     | **가젯티어 구성 및 "확률적" 인식**<br />2음절 물품 인식 향상 |
  |                          비문 취약                           |               오타와 구어체 포함 테스트 데이터               |

* [(생략) 정규표현식 이렇게 개선했습니다](https://docs.google.com/spreadsheets/d/1k_f6CVlXx_g1fAPs1QrUPjXSceNic9Ch4wrM7A6uFZ4/edit#gid=0) 
* [(생략) 모델은 2가지를 설계하고 다중분류를 선택했습니다](https://docs.google.com/spreadsheets/d/16tIEfFqyrTM-KOLT4n5FTv1KIpj1HrDtbTy8KJxxW68/edit?usp=sharing) </br></br>

## Multiclass classification (다중 분류)
- 라벨 개수 : 4개
- 라벨 종류 : 날짜 / 품목 / 위치 / 가격
- 라벨링 방식 : 바로 분류하지 않고, 2단계 분류 방식을 통해 정확한 라벨에 배정될 확률을 높임  
  
  - 1단계 :point_right: 각 라벨 당 최고 확률 문장을 추출
    
    ![my-image](https://github.com/Seohee-Kim/KoBERT-EveryoneContract/assets/62201733/24c4a367-4f45-4f1d-bbbb-e9eb04a32f75)  
    
  - 2단계 :point_right:  추출된 문장에서 핵심 단어만 sorting
    
    ![my-image (1)](https://github.com/Seohee-Kim/KoBERT-EveryoneContract/assets/62201733/a84065f5-6097-48ae-9b9b-93d69f601e2d)
    
- 핵심 모듈
  - `KoBERT`
    
  - `KSS` : 같은 턴 내의 문장을 재분리, ‘안녕하세요’와 같은 문장을 제거하여 핵심어 추출 범위를 보다 정확하게 함
    
  - `Komoran` : 사용자 명사 사전을 추가하여 명사 태깅 </br></br>

## 모델링 및 함수 보완

### 모델링 

* 라벨링을 위한 약 800개 수작업 전처리

* Train:Test = 8:2

* 하이퍼파라미터 설정

  ```python
  max_len = 64
  batch_size = 64
  warmup_ratio = 0.1
  num_epochs = 10
  max_grad_norm = 1
  log_interval = 200
  learning_rate =  5e-5
  ```  

### 함수 보완

* TimeChanger : 상대적 시간을 절대적 시간으로 변경 ('다음주 금요일'-> '10월 22일')
  
* WordMaker : 단어 조합 중 물품일 확률이 가장 높은 단어를 채택, 2음절 이상의 단어 인식 ('갤럭시'만 사전에 있어도 '갤럭시 버즈' 인식) </br></br>


## 장고 페이지 제작
### 목표

* 장고 웹페이지 배포를 통해 채팅 모델 테스트 환경을 만들고 시나리오 데이터를 수집

  * 모델 성능을 모두가 테스트할 수 있는 환경이 필요

  * 발생 가능한 스크립트 경우의 수를 넓힌 시나리오 데이터 수집 

### 구현

* UI : 카톡 대화 생성기처럼 대화의 입력값을 핑퐁 구현 (화자 선택 셀렉 박스, 대화 입력칸, 대화 종료 버튼, 채팅 결과창)
  
* DB : 시나리오 수집 (입력 및 결과 저장), 사용자를 위한 히스토리 페이지 구성

* 결과 페이지 : main, chat, history, about
  
  * 모듈은 KobertModule에서 일괄 관리, 버전 업그레이드가 필요한 모듈 별도 파일 구성
    
  * 인물 아이콘을 선택하여 입력 화자를 선택 및 변경, 채팅 입력란에 시나리오 입력
    
  * 계약서 생성 버튼을 눌러 채팅 종료, 모델 러닝 이후 우측에 요약 결과 표시

    ![my-image (2)](https://github.com/Seohee-Kim/KoBERT-EveryoneContract/assets/62201733/631d86e1-6676-4bcc-ae85-f935be0d52b4)
    
    ![my-image (3)](https://github.com/Seohee-Kim/KoBERT-EveryoneContract/assets/62201733/0667e015-1562-4870-97ea-a2791a26d1fb) </br></br>

</br></br>
## 피드백
* Q. 제조사 모델 반영 가능한지?  
	* A. 한국어에 특화된 데이터 셋이 부재하므로 상업적 이용 가능한 데이터 셋이 필요, 직접 구축하거나 위키 참조할 필요 있음
  
* Q. 외래어 등 다양한 상품 이름을 인식 가능할지?  
	* A. 관련된 타겟 물품 모델링 학습을 진행 시 정확도 개선 가능
  
* Q. 가격 네고 시 정규표현식으로 물품의 가격을 캐치하는 것이 가능할지?  
	* A. 현재로서는 불가능
 	* cf. 모델링 설계 단계부터 최종 승인 가격 캐치에 대한 고민이 많았는데, 그 중  한 가지 방법으로 가격 다음에 나오는 어절에 대한 감성 분석을 진행하여, 긍정일 경우에만 해당 가격을 최종 가격으로 캐치하는 방안을 생각했었는데 고도화하지 않아 실현하지 못함. 해당 질문은 가격 다음에 어떤 특정 어절을 정규표현식으로 캐치하여 최종 가격 판별 여부를 결정하는 거였는데, 마찬가지로 오타나 same meaning different expression 일 경우에 대한 가짓수에 대한 해결책이 없어 불가능하다고 답변

</br></br>
## 참고한 레퍼런스  
* https://github.com/wanasit/chrono
* https://velog.io/@dojun527/AWS-EC2-Django-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EB%B0%B0%ED%8F%AC%ED%95%98%EA%B8%B0
