from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('after/', views.post_view,name='after'),
    path('',views.index, name='index'),
]
