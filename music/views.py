from .models import Album, Song
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .forms import AlbumForm, SongForm, UserForm
from django.db.models import Q
from django.http import HttpResponse

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        albums = Album.objects.filter(user=request.user)
        songResults = Song.objects.all()
        query = request.GET.get("q")
        if(query):
            albums = albums.filter(
                Q(albumTitle__icontains = query)|
                Q(artist__icontains = query)
            ).distinct()

            songResults = songResults.filter(
                Q(songTitle__icontains = query)
            ).distinct()

            return render(request, 'music/index.html', {
                'albums': albums,
                'songs': songResults,
            })
        else:
            return render(request, 'music/index.html', {'albums': albums})



def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
    context = {
        'form': form,
    }
    return render(request, 'music/register.html', context)


def loginUser(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid Credentials !!!'})

    return render(request, 'music/login.html')



def logoutUser(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        'form': form,
    }
    return render(request, 'music/login.html', context)



def createAlbum(request):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.albumLogo = request.FILES['albumLogo']
            fileType =  album.albumLogo.url.split('.')[-1]
            fileType = fileType.lower()
            #album.albumLogo.url = album.albumTitle + '.' + fileType
            if fileType not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be of type JPG, JPEG or PNG !!!',
                }
                return render(request, 'music/createAlbum.html', context)
            album.save()
            return render(request, 'music/albumDetails.html', {'album': album})
        context = {
            'form': form,
        }
        return render(request, 'music/createAlbum.html', context)



def createSong(request, albumId):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=albumId)
    if form.is_valid():
        albumSongs = album.song_set.all()
        for s in albumSongs:
            if s.songTitle == form.cleaned_data.get('songTitle'):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Song already exists in the album !!!'
                }
                return render(request, 'music/createSong.html', context)
        song = form.save(commit=False)
        song.album = album
        song.audioFile = request.FILES['audioFile']
        fileType = song.audioFile.url.split('.')[-1]
        fileType = fileType.lower()
        #song.audioFile.url = song.songTitle + '.' + fileType
        if fileType not in AUDIO_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be of type WAV, MP3 or OGG !!!',
            }
            return render(request, 'music/createSong.html', context)

        song.save()
        return render(request, 'music/albumDetails.html', {'album': album})

    context = {
        'album':album,
        'form': form,
    }
    return render(request, 'music/createSong.html', context)



def deleteAlbum(request, albumId):
    album = Album.objects.get(pk=albumId)
    album.delete()
    albums = Album.objects.filter(user=request.user)
    return render(request, 'music/index.html', {'albums': albums})



def deleteSong(request, albumId, songId):
    album = get_object_or_404(Album, pk=albumId)
    song = Song.objects.get(pk=songId)
    song.delete()
    return render(request, 'music/albumDetails.html', {'album': album})



def favoriteSong(request, songId):
    song = get_object_or_404(Song, pk=songId)
    try:
        if song.isFavorite:
            song.isFavorite = False
        else:
            song.isFavorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})



def favoriteAlbum(request, albumId):
    album = get_object_or_404(Album, pk=albumId)
    try:
        if album.isFavorite:
            album.isFavorite = False
        else:
            album.isFavorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def albumDetails(request, albumId):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=albumId)
        context = {
            'user': user,
            'album': album,
        }
        return render(request, 'music/albumDetails.html', context)



def songs(request, filterBy):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        try:
            songIds = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    songIds.append(song.pk)

            usersSongs = Song.objects.filter(pk__in=songIds)
            if filterBy == 'favorites':
                usersSongs = Song.objects.filter(isFavorite=True)

        except Album.DoesNotExist:
            usersSongs = []

        return render(request, 'music/songs.html', {
            'songList': usersSongs,
            'filterBy': filterBy,
        })
