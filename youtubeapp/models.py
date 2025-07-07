from django.db import models
from django.core.validators import MinValueValidator

class Channel(models.Model):
    id = models.AutoField(primary_key=True)
    channel_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    thumbnail = models.URLField(max_length=200)
    description = models.CharField(max_length=500)
    subscriber_count = models.BigIntegerField(validators=[MinValueValidator(0)])
    video_count = models.BigIntegerField(validators=[MinValueValidator(0)])
    views_count = models.BigIntegerField(validators=[MinValueValidator(0)])

class VideoId(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=20)
    publish_time = models.DateTimeField()

class ExternalLinks(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    image_link = models.URLField(max_length=200)
    external_link = models.URLField(max_length=200)

class Videos(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    view_count = models.BigIntegerField()
    like_count = models.BigIntegerField()
    comment_count = models.IntegerField()
    publish_time = models.DateTimeField()
    is_shorts = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
