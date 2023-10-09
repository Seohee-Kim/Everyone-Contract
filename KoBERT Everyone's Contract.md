# KoBERT Everyone's Contract
* 중고거래 리카르디안 계약서 생성 - 채팅 내 핵심어 자동추출 모델
* Overview  
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
* **💻 코드** :  [모델링](https://github.com/Seohee-Kim/KoBERT-EveryoneContract/blob/main/Everyones_Contract_Classifier(v4).ipynb)   
* **💻 코드** :  [함수](https://github.com/Seohee-Kim/KoBERT-EveryoneContract/tree/main/pages/KobertModule)
* **💻 발표자료**  : [1차 발표](https://github.com/Seohee-Kim/KoBERT-EveryoneContract/blob/main/KoBERT%201%E1%84%8E%E1%85%A1%20%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA%20%E1%84%87%E1%85%A9%E1%84%80%E1%85%A9.pdf) </br></br>

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
  - 2단계 :point_right:  추출된 문장에서 핵심 단어만 sorting
- 핵심 모듈
  - `KoBERT` 
  - `KSS` : 같은 턴 내의 문장을 재분리, ‘안녕하세요’와 같은 문장을 제거하여 핵심어 추출 범위를 보다 정확하게 함
  - `Komoran` : 사용자 명사 사전을 추가하여 명사 태깅 </br></br>

<img>

<img>



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
  * 모듈은 KobertModule에서 일괄 관리하되, 버전 업그레이드가 필요한 모듈은 별도 파일로 구성했어요.
  * 인물 아이콘을 선택하여 입력 화자를 선택 및 변경할 수 있고, 채팅 입력란에 원하는 시나리오를 입력할 수 있어요.
  * 계약서 생성 버튼을 눌러 채팅을 종료할 수 있으며, 약간의 시간을 기다리면 우측에 요약 결과가 표시되어요.

<img> 

<img>

</br></br>

## 참고한 레퍼런스

* 