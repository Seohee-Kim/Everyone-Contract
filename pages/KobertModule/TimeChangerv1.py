from datetime import timezone, timedelta, date


class TimeChangerv1:

    def __init__(self):
        pass

    def get_yyyy(self):
        return date.today().year

    def get_mm(self):
        return date.today().month

    def get_dd(self):
        return date.today().day

    def get_wed(self):  # 요일 get func
        def num2wed(num):
            if num == 1:
                return '월요일'
            elif num == 2:
                return '화요일'
            elif num == 3:
                return '수요일'
            elif num == 4:
                return '목요일'
            elif num == 5:
                return '금요일'
            elif num == 6:
                return '토요일'
            else:
                return '일요일'

        num = date.today().isoweekday()  # 월 -> 1, 화 -> 2 ...
        wed = num2wed(num)
        return wed

    def timechanger(self, str):
        ### input -> string (예제 string은 TEST 2 참조) ###
        list1 = ['내일', '하루', '다음날', '명일', '명천', '이튿', '낼', ]  # 1일 뒤
        list2 = ['내일모레', '모레', '명후일', '재명일', '이틀']  # 2일 뒤
        list3 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']  # 단순 숫자
        list4 = ['다음주', '다음 주', '담주', '차주', '일주일', '칠일', '한 주일']  # 일주일
        ambig = ['중', '쯤', '내']
        list5 = ['사흘', '나흘', '닷새', '엿새', '이레', '여드레', '아흐레', '열흘']

        now = date.today()
        num_today = date.today().isoweekday()

        for i in list1:
            if i in str:
                return now + timedelta(days=1)

        for i in list2:
            if i in str:
                return now + timedelta(days=2)

        for i in list3:
            if i in str:
                return now + timedelta(days=int(i))

        for i in list4:
            if i in str:
                if ambig in list(str):
                    # print(list(str))
                    print('모호한 표현입니다. 날짜 변환이 불가능합니다.')
                elif '월요일' in str:
                    moving_num = 8 - int(num_today)  # 오늘이 1 이라면 +7 만큼 이동, 2 라면 +6 만큼 이동
                    return now + timedelta(days=moving_num)
                elif '화요일' in str:
                    moving_num = 9 - int(num_today)  # 오늘이 1 이라면 +8 만큼 이동, 2 라면 +7 만큼 이동
                    return now + timedelta(days=moving_num)
                elif '수요일' in str:
                    moving_num = 10 - int(num_today)
                    return now + timedelta(days=moving_num)
                elif '목요일' in str:
                    moving_num = 11 - int(num_today)
                    return now + timedelta(days=moving_num)
                elif '금요일' in str:
                    moving_num = 12 - int(num_today)
                    return now + timedelta(days=moving_num)
                elif '토요일' in str:
                    moving_num = 13 - int(num_today)
                    return now + timedelta(days=moving_num)
                elif '일요일' in str:
                    moving_num = 14 - int(num_today)
                    return now + timedelta(days=moving_num)
                else:
                    return now + timedelta(days=7)

        for j in range(0, len(list5) - 1):
            if list5[j] in str:
                days = j + 3
                return now + timedelta(days=days)
