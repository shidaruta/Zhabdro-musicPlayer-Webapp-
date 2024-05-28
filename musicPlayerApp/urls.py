from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('albums/', views.albums, name='albums'),
    path('favorite/', views.favorites, name='favorite'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('toggle_favorite/<int:song_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('search/', views.search_view, name='search'),
    path('album/<int:album_id>/add_song/', views.add_song, name='add_song'),
    path('delete_song/<int:song_id>/', views.delete_song, name='delete_song'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('delete_album/<int:album_id>/', views.delete_album, name='delete_album'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

