from django.shortcuts import render
from blog import models
import random
from django.db.models import Q
from django.http import HttpResponse
from blog.forms import UploadForm
from .apps import BlogConfig
import os

# Create your views here.
def post_view(request):
    random_index1 = int(random.random() * 10) + 1
    random_index2 = (random_index1+1)%10+1
    posts = models.Song.objects.filter(Q(field_id=random_index1)|Q(field_id=random_index2))  # Song 테이블의 모든 객체 불러옴

    return render(request, 'after.html', {"posts":posts})


def index(request):
    if request.method=='POST':
        form=UploadForm(request.POST,request.FILES)
        if form.is_valid():
            convs=form.save(commit=False)
            convs.save()
            path_convs=convs.kakao_conversation.url.encode('utf-8')[1:]
            username=convs.user_name
            result=BlogConfig.predictor.predict(user_name=username,conversation_path=path_convs)
            os.remove(path_convs)
            print(result)
            return HttpResponse((result[0]+" and "+result[1]))
            #return redirect('success')
    else:
        form=UploadForm()
    return render(request,'index.html',{
        'form':form
    })
