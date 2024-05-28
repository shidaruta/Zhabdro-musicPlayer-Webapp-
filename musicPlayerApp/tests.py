from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Album, Comment, Song, Favorite
from datetime import timedelta

class ModelsTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create(username='test_user', password='test_password')
        
        # Create an album
        self.album = Album.objects.create(user=self.user, album_title='Test Album', album_logo='test_logo.jpg')
        
        # Create a song
        self.song = Song.objects.create(album=self.album, song_title='Test Song', audio_file='test_song.mp3')
        
        # Create a comment
        self.comment = Comment.objects.create(album=self.album, user=self.user, content='Test comment')
        
        # Create a favorite
        self.favorite = Favorite.objects.create(user=self.user, song=self.song)
    
    def test_album_creation(self):
        self.assertEqual(self.album.user, self.user)
        self.assertEqual(self.album.album_title, 'Test Album')
    
    def test_comment_creation(self):
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.album, self.album)
        self.assertEqual(self.comment.content, 'Test comment')
    
    def test_song_creation(self):
        self.assertEqual(self.song.album, self.album)
        self.assertEqual(self.song.song_title, 'Test Song')
    
    def test_favorite_creation(self):
        self.assertEqual(self.favorite.user, self.user)
        self.assertEqual(self.favorite.song, self.song)
    
    def test_comment_date(self):
        # Test comment creation date is within the last minute
        time_difference = timezone.now() - self.comment.created_at
        self.assertTrue(time_difference < timedelta(minutes=1))

# Run tests by running "python manage.py test" in your Django project directory
