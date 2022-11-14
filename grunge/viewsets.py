from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .filters import AlbumFilter, ArtistFilter, TrackFilter, PlaylistFilter
from .models import Album, Artist, Track, Playlist
from .serializers import AlbumSerializer, ArtistSerializer, TrackSerializer, PlaylistSerializer


class BaseAPIViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"


class ArtistViewSet(BaseAPIViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    filter_class = ArtistFilter


class AlbumViewSet(BaseAPIViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filter_class = AlbumFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("artist").prefetch_related("tracks")


class TrackViewSet(BaseAPIViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    filter_class = TrackFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("album", "album__artist")


class PlaylistViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    filter_class = PlaylistFilter

    def create(self, request, *args, **kwargs):
        tracks_id_list = request.data["tracks"]
        _serializer = self.serializer_class(data=request.data,
                                            context={'tracks': tracks_id_list,
                                                     'request': request})
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        tracks_id_list = request.data["tracks"]
        _serializer = self.serializer_class(data=request.data,
                                            context={'tracks': tracks_id_list,
                                                     'request': request})
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        tracks_id_list = request.data.get("tracks")
        _serializer = self.serializer_class(data=request.data,
                                            context={'tracks': tracks_id_list,
                                                     'request': request})
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
