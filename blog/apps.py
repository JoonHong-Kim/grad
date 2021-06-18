from django.apps import AppConfig
from .kobertprediction import KoBERTPredictor


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    predictor= KoBERTPredictor(model_path="blog/model/best-epoch-36-f1-0.732.bin")

