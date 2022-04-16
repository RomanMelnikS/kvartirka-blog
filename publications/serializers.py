from rest_framework import serializers

from .models import Publication, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        source='author.username',
        read_only=True
    )
    replays = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'text',
            'created',
            'replays'
        )

    def get_replays(self, obj):
        queryset = Comment.objects.filter(
            replays_id=obj.id
        )
        serializer = CommentSerializer(
            queryset,
            many=True
        )
        return serializer.data


class ReplaysCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            'author',
            'text',
            'replays',
            'publication'
        )

    def to_representation(self, instance):
        serializer = CommentSerializer(instance)
        return serializer.data


class PublicationSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        source='author.username',
        read_only=True
    )
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = (
            'author',
            'text',
            'created',
            'comments'
        )

    def get_comments(self, obj):
        queryset = Comment.objects.filter(
            publication_id=obj.id,
            replays_id=None
        )
        serializer = CommentSerializer(
            queryset,
            many=True
        )
        return serializer.data
