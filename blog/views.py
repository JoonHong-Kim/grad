from django.shortcuts import render, redirect
from blog import models
import random
from django.db.models import Q
from django.http import HttpResponse
from blog.forms import UploadForm
from .apps import BlogConfig
import os

# Create your views here.
#감정 1순위 2순위
emotion1,emotion2='',''
def post_view(request):

    if emotion1 == 'happy':
        random_index1 = int(random.random() * 10) + 1
        if (random_index1+1)==11:
            random_index2 = (random_index1 + 1) % 11 + 1
        else:
            random_index2=random_index1+1
    elif emotion1 == 'fear':
        random_index1 = int(random.random() * 10) + 11
        if (random_index1+1)==21:
            random_index2 = (random_index1 + 1) % 21 + 11
        else:
            random_index2=random_index1+1
    elif emotion1 == 'sad':
        random_index1 = int(random.random() * 10) + 21
        if (random_index1+1)==31:
            random_index2 = (random_index1 + 1) % 31 + 21
        else:
            random_index2=random_index1+1
    else: # angry
        random_index1 = int(random.random() * 4) + 31
        if (random_index1+1)==35:
            random_index2 = (random_index1 + 1) % 35 + 31
        else:
            random_index2=random_index1+1
    posts = models.Song.objects.filter(Q(field_id=random_index1)|Q(field_id=random_index2))  # Song 테이블의 모든 객체 불러옴

    #print("emotion1 =",emotion1,'emotion2 = ',emotion2)
    if emotion2 == 'happy':
        random_index3 = int(random.random() * 10) + 1
        if (random_index3 + 1) == 11:
            random_index4 = (random_index3 + 1) % 11 + 1
        else:
            random_index4 = random_index3 + 1
    elif emotion2 == 'fear':
        random_index3 = int(random.random() * 10) + 11
        if (random_index3 + 1) == 21:
            random_index4 = (random_index3 + 1) % 21 + 11
        else:
            random_index4 = random_index3 + 1
    elif emotion2 == 'sad':
        random_index3 = int(random.random() * 10) + 21
        if (random_index3 + 1) == 31:
            random_index4 = (random_index3 + 1) % 31 + 21
        else:
            random_index4 = random_index3 + 1
    else:  # angry
        random_index3 = int(random.random() * 4) + 31
        if (random_index3 + 1) == 35:
            random_index4 = (random_index3 + 1) % 35 + 31
        else:
            random_index4 = random_index3 + 1
    posts1 = models.Song.objects.filter(Q(field_id=random_index3)|Q(field_id=random_index4))  # Song 테이블의 모든 객체 불러옴

    if emotion1=='happy':
        emotion_kor1='행복한'
    elif emotion1== 'fear' :
        emotion_kor1='무서운'
    elif emotion1== 'sad':
        emotion_kor1='슬픈'
    else:
        emotion_kor1='화난'

    if emotion2=='happy':
        emotion_kor2='행복한'
    elif emotion2== 'fear' :
        emotion_kor2='무서운'
    elif emotion2== 'sad':
        emotion_kor2='슬픈'
    else:
        emotion_kor2='화난'

    print(random_index1, random_index2, random_index3, random_index4)

    #render : 템플릿에 전달하는 것
    return render(request, 'after.html', {"posts":posts,
                                          "posts1":posts1,
                                          "emotion1":emotion_kor1,
                                        "emotion2":emotion_kor2})
def index(request):
    if request.method=='POST':
        form=UploadForm(request.POST,request.FILES)
        if form.is_valid():
            #convs= 대화파일
            convs=form.save(commit=False)
            convs.save()

            #파일명 깨지는거 해결
            path_convs=convs.kakao_conversation.url.encode('utf-8')[1:]

            #입력받은 사용자 이름
            username=convs.user_name

            #감정1 감정2 추측
            result=BlogConfig.predictor.predict(user_name=username,conversation_path=path_convs)

            #필요없으므로 삭제
            os.remove(path_convs)

            #감정 1순위 2순위를 global 변수로 넘겨줌
            global emotion1
            global emotion2
            emotion1=result[0]
            emotion2=result[1]
            print(result)
            return redirect('after')
    #파일 안올렸을 때
    else:
        form=UploadForm()
    return render(request,'index.html',{
        'form':form
    })
