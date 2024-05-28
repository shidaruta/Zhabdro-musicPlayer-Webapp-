from django.db import models
from django.contrib.auth.models import User

class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album_title = models.CharField(max_length=500)
    album_logo = models.ImageField(upload_to='photos/')
    
    def __str__(self):
        return f"{self.album_title} - {self.user.username}"

class Comment(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.album.album_title}"

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='', upload_to='songs/')
    
    def __str__(self):
        return self.song_title

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} favorited {self.song.song_title}"
