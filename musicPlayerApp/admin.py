from django.contrib import admin
from .models import Album, Song, Favorite
from django.utils.html import format_html

class AlbumAdmin(admin.ModelAdmin):
    def album_logo_tag(self, obj):
        return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.album_logo.url))
    album_logo_tag.short_description = 'Album Logo'

    def user_name(self, obj):
        return obj.user.username
    user_name.short_description = 'Artist'

    list_display = ['album_title', 'user_name', 'album_logo_tag']

admin.site.register(Album, AlbumAdmin)

class SongAdmin(admin.ModelAdmin):
    list_display = ('song_title', 'album', 'display_album_logo', 'is_favorited')
    list_filter = ('album', )
    search_fields = ('song_title', 'album__album_title')

    def display_album_logo(self, obj):
        if obj.album.album_logo:
            return format_html('<img src="{}" alt="Album Logo" height="50">'.format(obj.album.album_logo.url))
        else:
            return '-'
    display_album_logo.short_description = 'Album Logo'

    def is_favorited(self, obj):
        return Favorite.objects.filter(song=obj).exists()
    is_favorited.boolean = True
    is_favorited.short_description = 'Is Favorited'

admin.site.register(Song, SongAdmin)