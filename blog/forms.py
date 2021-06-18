from django import forms
from .models import KakaoUpload

class UploadForm(forms.ModelForm):
    class Meta:
        model = KakaoUpload
        fields={'user_name','kakao_conversation'}