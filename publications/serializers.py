from rest_framework import serializers

from .models import Comment, Publication


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

    def get_replays(self, instance):
        request = self.context['request']
        level = request.query_params.get('level')
        queryset = Comment.objects.filter(
            replays_id=instance.id
        )
        if level:
            filtered_queryset = queryset.filter(
                level__lte=level
            )
            serializer = CommentSerializer(
                filtered_queryset,
                context=self.context,
                many=True
            )
            return serializer.data
        serializer = CommentSerializer(
            queryset,
            context=self.context,
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
        serializer = CommentSerializer(
            instance,
            context=self.context,
        )
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
            context=self.context,
            many=True
        )
        return serializer.data
