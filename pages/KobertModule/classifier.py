import torch
from torch.utils.data import Dataset
import gluonnlp as nlp
import numpy as np
from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model
import re
import kss
from pages.KobertModule.BERTClasses import BERTClassifier, BERTDataset
from pages.KobertModule.TimeChangerv1 import TimeChangerv1 as tc

#CPU 디바이스 사용
device = torch.device('cpu')

#Bert 모델 로드
bertmodel, vocab = get_pytorch_kobert_model()

#학습된 모델 로드
MODELPATH = "pages\KobertModule\kobertModel_for_Django.pt"
model = BERTClassifier(bertmodel,  dr_rate=0.5).to(device)
model.load_state_dict(torch.load(MODELPATH, map_location='cpu'))
model.eval()

#토큰화
tokenizer = get_tokenizer()
tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)

#형태소 분석기
from PyKomoran import Komoran
komoran = Komoran("EXP")
komoran.set_user_dic(r"pages\KobertModule\user_dic.txt")

#파라미터 설정
max_len = 64
batch_size = 64
warmup_ratio = 0.1
num_epochs = 10
max_grad_norm = 1
log_interval = 200
learning_rate =  5e-5

# 날짜, 품목, 위치, 가격
def predict2(sent):
    data = [sent, '0']
    dataset_another = [data]
    another_test = BERTDataset(dataset_another, 0, 1, tok, max_len, True, False)
    test_dataloader = torch.utils.data.DataLoader(another_test, batch_size=batch_size, num_workers=0)
    model.eval()
    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(test_dataloader):
        token_ids = token_ids.long().to(device)
        segment_ids = segment_ids.long().to(device)
        valid_length= valid_length
        label = label.long().to(device)
        out = model(token_ids, valid_length, segment_ids)
        test_eval=[]
        for i in out:
            logits = i
            logits = logits.detach().cpu().numpy()
            if np.argmax(logits) == 0:
                test_eval.append("날짜")
            elif np.argmax(logits) == 1:
                test_eval.append("위치")
            elif np.argmax(logits) == 2:
                test_eval.append("품목")
            elif np.argmax(logits) == 3:
                test_eval.append("가격")
        return test_eval[0], out

# 문장분리를 위한 kss
def KSS(sent):
    kss_sent = []
    for i in sent:
        j = kss.split_sentences(i)
        kss_sent.extend(j)
    #print('>> 원본 텍스트 <<')
    #for i in sent:
    #    print(i)

    #print('\n>> 분리 텍스트 <<')
    #for i in kss_sent:
    #    print(i)
    #print("\n\n")
    return kss_sent

# 다중 분류 수행 모듈
class ClassifierModule():
    def __init__(self):
        self.text = ""

        self.date_sent = ""  # sorting()
        self.item_sent = ""
        self.place_sent = ""
        self.price_sent = ""

        self.words = []  #sentence_to_words(): 명사 리스트

        self.date_word = ""
        self.item_words = []
        self.item_word = ""
        self.place_word = ""
        self.price_word = ""

    #모델 재사용시 이전 계약서 정보가 넘어오지 않도록 하기 위한 reset
    def reset_variables(self):
        self.text = ""

        self.date_sent = ""
        self.item_sent = ""
        self.place_sent = ""
        self.price_sent = ""

        self.words = []

        self.date_word = ""
        self.item_words = []
        self.item_word = ""
        self.place_word = ""
        self.price_word = ""


    def sentence_to_words(self):  ## 선정된 문장에 대해 명사만 추출하여 리스트 생성
        self.words = komoran.nouns(self.date_sent) + komoran.nouns(self.item_sent) + komoran.nouns(self.place_sent)
        print(self.words)

    def sorting(self):  ## 전체 문장 리스트에 대해 정확도가 가장 높은 문장 분류
        date_max = -1
        item_max = -1
        place_max = -1
        price_max = -1

        text_after_KSS = KSS(self.text)
        for sent in text_after_KSS:
            test_eval, out = predict2(sent)
            max_val, max_index = torch.max(out, 1)
            # print(sent)
            # print(max_val)
            # print("\n")

            if test_eval == '날짜':
                if date_max < max_val:
                    self.date_sent = sent
                    date_max = max_val
            elif test_eval == '품목':
                if item_max < max_val:
                    item_max = max_val
                    self.item_sent = sent
            elif test_eval == '위치':
                if place_max < max_val:
                    place_max = max_val
                    self.place_sent = sent
            elif test_eval == '가격':
                if price_max < max_val:
                    self.price_sent = sent

        print(
            '>> 문장만 Sorting <<',
            '\n날짜 정보 : ', self.date_sent,
            '\n품목 정보 : ', self.item_sent,
            '\n위치 정보 : ', self.place_sent,
            '\n가격 정보 : ', self.price_sent)

    def final_check(self):
        if self.price_word == "":
            money_regex = re.compile("\d+(원|만원|마넌)|\d+만|만원|\d+.\d(만원|만)?")
            for sent in self.text:
                result = money_regex.search(sent)
                if result:
                    self.price_word = result.group(0)

    def word_maker(self, word_list):
        if len(word_list) == 0:
            return "";
        if len(word_list) == 1:
            return word_list[0][0]
        word_list = sorted(word_list, key=lambda x:x[1], reverse=True)
        candidates = [word_list[0][0], word_list[0][0] + " " + word_list[1][0], word_list[1][0]+ " " + word_list[0][0]]
        candidates_and_value = []
        for candidates in candidates:
            test_eval, out = predict2(candidates)
            max_val, max_index = torch.max(out,1)
            candidates_and_value.append([candidates, max_val])
        candidates_and_value = sorted(candidates_and_value, key=lambda x:x[1], reverse=True)
        return candidates_and_value[0][0]

    def words_sorting(self, text):  ## 명사 리스트 중에서 가장 정확도가 높은 명사 분류
        self.reset_variables()
        self.text = text
        self.sorting()
        self.sentence_to_words()
        date_max = -1
        item_max = -1
        place_max = -1
        price_max = -1
        for word in self.words:
            test_eval, out = predict2(word)
            max_val, max_index = torch.max(out, 1)
            # print(word)
            # print(max_val)
            # print("\n")

            if test_eval == '날짜':
                if self.date_word == "" and date_max < max_val:
                    self.date_word = word
                    date_max = max_val

            elif test_eval == '품목':
                self.item_words.append([word, max_val])

            elif test_eval == '위치':
                if place_max < max_val:
                    self.place_word = word
                    place_max = max_val

        #품목 후보 리스트에서 정확도가 가장 높은 품목 명사 추출
        self.item_word = self.word_maker(self.item_words)

        # 정규표현식 날짜 추출 + timechanger
        date_regex = re.compile("(\d+월)? \d+일")
        result = date_regex.search(self.date_word)
        if result:
            self.date_word = self.date_word
        else:
            new_date_sent = str(self.date_sent)
            self.date_word = str(tc().timechanger(new_date_sent))
            self.date_word = self.date_word

        # 정규표현식을 통한 실제 가격 추출
        money_regex = re.compile("\d+(원|만원|마넌)|\d+만|만원|\d+.\d(만원|만)?")
        result = money_regex.search(self.price_sent)
        if result:
            self.money_word = result.group(0)

        self.final_check()

        print(
            '>> 핵심 단어만 Sorting <<',
            '\n날짜 정보 : ', self.date_word,
            '\n품목 정보 : ', self.item_word,
            '\n위치 정보 : ', self.place_word,
            '\n가격 정보 : ', self.price_word)

        contract_dic = {'date': self.date_word, 'item': self.item_word, 'location': self.place_word, 'price': self.price_word}
        return contract_dic