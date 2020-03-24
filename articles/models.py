from django.db import models
from django.conf import settings
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = ProcessedImageField(
                null=True, # 필드값 유효성검사할 때 빈값도 가능
                blank=True, # 모델폼 입력할 때 빈값도 가능
                processors=[ResizeToFill(300,300)], # 비율이 안깨지게(리스트형태)
                format='JPEG',
                options={'quality':90}, # 생략해도 상관없음
                upload_to='articles' # 경로
            )
    info = models.BooleanField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')
    views = models.IntegerField(default=0)
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    image = ProcessedImageField(
                null=True, # 필드값 유효성검사할 때 빈값도 가능
                blank=True, # 모델폼 입력할 때 빈값도 가능
                processors=[ResizeToFill(100,100)], # 비율이 안깨지게(리스트형태)
                format='JPEG',
                options={'quality':90}, # 생략해도 상관없음
                upload_to='articles' # 경로
            )

# class Like(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
#     article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)