from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Publication
from .serializers import PublicationSerializer, CommentSerializer


class PublicationsViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all().order_by('-created')
    serializer_class = PublicationSerializer

    def perform_create(self, serializer):
        data = {
            'author': self.request.user
        }
        serializer.save(**data)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        publication_id = self.kwargs.get('publication_id')
        publication = get_object_or_404(Publication, id=publication_id)
        queryset = publication.comments.filter(replays_id=None)
        return queryset

    def perform_create(self, serializer):
        publication_id = self.kwargs.get('publication_id')
        publication = get_object_or_404(Publication, id=publication_id)
        data = {
            'author': self.request.user,
            'publication': publication,
        }
        serializer.save(**data)
