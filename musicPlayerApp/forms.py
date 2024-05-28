from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Album, Song

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1', 'password2']

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['album_title', 'album_logo']
        labels = {
            'album_title': '',
            'album_logo':'',
        }

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['song_title', 'audio_file']

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 1}), label='')
