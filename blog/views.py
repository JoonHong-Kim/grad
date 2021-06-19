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
    random_index1 = int(random.random() * 10) + 1
    random_index2 = (random_index1+1)%10+1
    posts = models.Song.objects.filter(Q(field_id=random_index1)|Q(field_id=random_index2))  # Song 테이블의 모든 객체 불러옴
    print("emotion1 =",emotion1,'emotion2 = ',emotion2)
    return render(request, 'after.html', {"posts":posts})


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

            return redirect('after')
            #return redirect('success')
    #파일 안올렸을 때
    else:
        form=UploadForm()
    return render(request,'index.html',{
        'form':form
    })
