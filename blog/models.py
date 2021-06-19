from django.db import models
import os


class Song(models.Model):
    field_id = models.AutoField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    emotion_type = models.CharField(max_length=16, blank=True, null=True)
    song_url = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'song'


# Create your models here.
def up_to(instance, filename):
    return os.path.join('', 'tmp')


class KakaoUpload(models.Model):
    user_name = models.CharField(max_length=100,null=False)
    kakao_conversation = models.FileField(upload_to=up_to)
