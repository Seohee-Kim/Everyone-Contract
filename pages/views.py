from django.shortcuts import render, redirect
from pages.models import Contract, Message
from .apps import PagesConfig
# Create your views here.

def Main(request):
    return render(request, "main.html")


def Chat(request):
    if request.method == "POST":
        print(request.POST)
        if request.POST['text'] == "":
            return redirect('chat')
        msg = Message()
        msg.talker = request.POST['talker']
        msg.msg = request.POST['text']
        msg.save()
        return redirect('chat')
    else:
        messages = Message.objects.all()
        return render(request, "chat.html", {'messages' : messages})


def makeContract(request):
    chatText = ""
    sent = []
    result = {'date': "", 'item': "", 'location': "", 'price': ""}

    #저장된 메시지 전부 호출
    messages = Message.objects.all()

    for message in messages:
        chatText += "[" + message.timestamp.strftime('%Y-%m-%d %H:%M') + "] " + message.talker + " : " + message.msg + "\n"
        sent.append(message.msg)

    #채팅이 하나도 없다면 계약서를 만들지 않음
    if chatText == "":
        return redirect('chat')

    # 문장 리스트화 한 메시지 분류 모델에 전달
    result = PagesConfig.classifiermodule.words_sorting(sent)

    #새 계약서 생성
    print(chatText)
    newContract = Contract()
    newContract.chats = chatText
    newContract.date = result['date']
    newContract.item = result['item']
    newContract.location = result['location']
    newContract.price = result['price']
    newContract.save()

    return render(request, "chat.html", {'messages' : messages, 'newContract': newContract})


def resetMessages(request):
    messages = Message.objects.all()
    messages.delete()

    return render(request, "chat.html")


def History(request):
    contracts = Contract.objects.all().order_by('id')
    return render(request, "history.html", {'contracts': contracts})



def Detail(request, pk):
    contract = Contract.objects.get(pk=pk)
    return render(request, 'detail.html', {'contract': contract})


def About(request):
    return render(request, "about.html")