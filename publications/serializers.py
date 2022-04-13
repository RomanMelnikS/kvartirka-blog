from rest_framework import serializers

from .models import Publication, Comment, User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
        )


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Comment
        exclude = (
            'publication',
        )


class PublicationSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    comments = CommentSerializer(many=True)

    class Meta:
        model = Publication
        fields = '__all__'
