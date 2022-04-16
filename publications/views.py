from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Comment, Publication
from .serializers import (CommentSerializer, PublicationSerializer,
                          ReplaysCreateSerializer)


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

    @action(
        detail=True,
        methods=['get', 'post'],
        name='replays',
        url_name='replays',
        url_path='replays'
    )
    def replays(self, request, publication_id, pk):
        user = self.request.user
        text = self.request.data.get('text')
        publication = get_object_or_404(
            Publication,
            id=publication_id
        )
        comment = get_object_or_404(
            Comment,
            id=pk
        )
        serializer = CommentSerializer(comment)
        if request.method == 'POST':
            serializer = ReplaysCreateSerializer(
                data={
                    'publication': publication.id,
                    'author': user.id,
                    'replays': comment.id,
                    'text': text
                },
                context={
                    'request': request
                }
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
