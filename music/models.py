from django.contrib.auth.models import User
from django.db import models

class Album(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    artist = models.CharField(max_length=255)
    albumTitle = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    albumLogo = models.FileField()
    isFavorite = models.BooleanField(default=False)

    def __str__(self):
        return self.albumTitle + '-' + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    songTitle = models.CharField(max_length=255)
    audioFile = models.FileField(default='')
    isFavorite = models.BooleanField(default=False)

    def __str__(self):
        return self.songTitle