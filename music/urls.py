from django.conf.urls import url
from . import views

app_name = 'music'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^loginUser/$', views.loginUser, name='loginUser'),
    url(r'^logout_user/$', views.logoutUser, name='logoutUser'),
    url(r'^createAlbum/$', views.createAlbum, name='createAlbum'),
    url(r'^(?P<albumId>[0-9]+)/createSong/$', views.createSong, name='createSong'),
    url(r'^(?P<albumId>[0-9]+)/$', views.albumDetails, name='albumDetails'),
    url(r'^songs/(?P<filterBy>[a-zA_Z]+)/$', views.songs, name='songs'),
    url(r'^(?P<songId>[0-9]+)/favoriteSong/$', views.favoriteSong, name='favoriteSong'),
    url(r'^(?P<albumId>[0-9]+)/deleteSong/(?P<songId>[0-9]+)/$', views.deleteSong, name='deleteSong'),
    url(r'^(?P<albumId>[0-9]+)/favoriteAlbum/$', views.favoriteAlbum, name='favoriteAlbum'),
    url(r'^(?P<albumId>[0-9]+)/deleteAlbum/$', views.deleteAlbum, name='deleteAlbum'),

]
