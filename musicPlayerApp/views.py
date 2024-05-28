from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from django.contrib import messages
from django.contrib.auth  import authenticate, login, logout

from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from .models import Album, Song, Comment, Favorite
from .forms import AlbumForm, CreateUserForm, SongForm, CommentForm


AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']

import random
@login_required(login_url='login')
def index(request):
    songs = list(Song.objects.all())
    random.shuffle(songs)
    
    if request.user.is_authenticated:
        favorited_songs = set(Favorite.objects.filter(user=request.user).values_list('song_id', flat=True))
    else:
        favorited_songs = set()

    for song in songs:
        song.is_favorite = song.id in favorited_songs

    context = {
        'songs': songs,
    }
    return render(request, 'index.html', context)

@login_required(login_url='login')
def search_view(request):
    query = request.GET.get('q', '')
    albums = []
    songs = []
    if len(query) > 2:
        albums = Album.objects.filter(album_title__icontains=query)
        songs = Song.objects.filter(song_title__icontains=query)
    context = {
        'albums': albums,
        'songs': songs,
        'query': query,
    }
    return render(request, 'search_result.html', context)

@csrf_exempt
@login_required(login_url='login')

def delete_song(request, song_id):
    if request.method == 'POST':
        song = get_object_or_404(Song, id=song_id)
        song.delete()
        return JsonResponse({'success': True})
    return HttpResponseNotAllowed(['POST'])

@require_POST
@login_required(login_url='login')

def toggle_favorite(request, song_id):
    song = Song.objects.get(id=song_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, song=song)
    
    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True
    
    return JsonResponse({'success': True, 'is_favorite': is_favorite})

@login_required(login_url='login')
def albums(request):
    albums = Album.objects.all()
    return render(request, 'album.html', {'albums': albums})

@login_required(login_url='login')
def delete_album(request, album_id):
    if request.method == 'POST':
        album = get_object_or_404(Album, pk=album_id)
        album.delete()
        return redirect('profile')
    return redirect('album_detail', album_id=album_id)  # Redirect to the album detail if not a POST request

@login_required(login_url='login')
def album_detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    songs = album.song_set.all()
    comments = album.comments.all()

    # Check if each song is favorited by the user
    favorite_song_ids = Favorite.objects.filter(user=request.user, song__in=songs).values_list('song_id', flat=True)
    for song in songs:
        song.is_favorite = song.id in favorite_song_ids

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            Comment.objects.create(
                album=album,
                user=request.user,
                content=content
            )
            return redirect('album_detail', album_id=album_id)
    else:
        form = CommentForm()

    context = {
        'album': album,
        'songs': songs,
        'comments': comments,
        'form': form,
    }
    return render(request, 'album_details.html', context)

@login_required(login_url='login')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:
        comment.delete()
    return redirect('album_detail', album_id=comment.album.id)

@login_required(login_url='login')
def add_song(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    songs = album.song_set.all()
    last_clicked_section = 'add-song'

    if request.method == 'POST':
        forms = SongForm(request.POST, request.FILES)
        audio_file = request.FILES.get('audio_file', None)
        
        if audio_file:
            file_type = audio_file.name.split('.')[-1].lower()
            if file_type in AUDIO_FILE_TYPES:
                if forms.is_valid():
                    new_song = forms.save(commit=False)
                    new_song.album = album
                    new_song.save()
                    messages.success(request, "Song added successfully.")
                    return redirect('add_song', album_id=album.id)
            else:
                messages.error(request, "Audio file must be WAV, MP3, or OGG.")
        
    else:
        forms = SongForm()
        print(forms.errors)  # Add this line to check for form errors

    context = {
        'album': album,
        'songs': songs,
        'forms': forms,
        'last_clicked_section': last_clicked_section,
    }
    return render(request, 'addsong.html', context)

@login_required(login_url='login')
def profile(request):
    albums = Album.objects.filter(user=request.user)
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.save()
            return redirect('profile')
        else:
            print(form.errors)
    else:
        form = AlbumForm()

    context = {
        'albums': albums,
        'form': form
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def favorites(request):
    favorited_songs = Favorite.objects.filter(user=request.user).select_related('song')
    for favorite in favorited_songs:
        favorite.song.is_favorite = True
    return render(request, 'favorites.html', {'favorited_songs': favorited_songs})

@unauthenticated_user
def registerPage(request):
    
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for '+user )
            return redirect('login')

    context={'form': form}
    return render(request, 'register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Print user object and session data
            print(request.user)
            print(request.session)
            return redirect('index')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')
