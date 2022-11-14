from furl import furl
from rest_framework import serializers
from rest_framework.reverse import reverse as drf_reverse

from .fields import UUIDHyperlinkedIdentityField
from .models import Album, Artist, Track, Playlist


class TrackAlbumArtistSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="artist-detail")

    class Meta:
        model = Artist
        fields = ("uuid", "url", "name")


class TrackAlbumSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="album-detail")
    artist = TrackAlbumArtistSerializer()

    class Meta:
        model = Album
        fields = ("uuid", "url", "name", "artist")


class TrackSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="track-detail")
    album = TrackAlbumSerializer()

    class Meta:
        model = Track
        fields = ("uuid", "url", "name", "number", "album")


class AlbumTrackSerializer(TrackSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="track-detail")

    class Meta:
        model = Track
        fields = ("uuid", "url", "name", "number")


class AlbumArtistSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="artist-detail")

    class Meta:
        model = Artist
        fields = ("uuid", "url", "name")


class AlbumSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="album-detail")
    artist = AlbumArtistSerializer()
    tracks = AlbumTrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ("uuid", "url", "name", "year", "artist", "tracks")


class ArtistSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="artist-detail")
    albums_url = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ("uuid", "url", "name", "albums_url")

    def get_albums_url(self, artist):
        path = drf_reverse("album-list", request=self.context["request"])
        return furl(path).set({"artist_uuid": artist.uuid}).url


class PlaylistSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="playlist-detail")
    tracks = TrackSerializer(many=True, read_only=True)

    def create(self, validated_data):
        tracks = self.context['tracks']
        instance = Playlist.objects.create(**validated_data)
        for track_id in tracks:
            track = Track.objects.filter(uuid=track_id).first()
            instance.tracks.add(track)
        return instance

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            update_name = validated_data.pop('name')
            if update_name:
                instance.name = update_name
                instance.save()
        tracks = self.context['tracks']
        if tracks:
            instance.tracks.clear()
            for track_id in tracks:
                track = Track.objects.filter(uuid=track_id).first()
                instance.tracks.add(track)
        return instance

    class Meta:
        model = Playlist
        fields = ("uuid", "url", "name", "tracks")
