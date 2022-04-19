from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Comment, Publication
from .serializers import (CommentSerializer, PublicationSerializer,
                          ReplaysCreateSerializer)


@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        operation_summary='Список публикаций',
        tags=['Публикации']
    )
)
@method_decorator(
    name='create',
    decorator=swagger_auto_schema(
        operation_summary='Добавить публикацию',
        tags=['Публикации']
    )
)
@method_decorator(
    name='retrieve',
    decorator=swagger_auto_schema(
        operation_summary='Детализация публикации',
        tags=['Публикации']
    )
)
@method_decorator(
    name='update',
    decorator=swagger_auto_schema(
        operation_summary='Обновить публикацию',
        tags=['Публикации']
    )
)
@method_decorator(
    name='partial_update',
    decorator=swagger_auto_schema(
        operation_summary='Обновить публикацию частично',
        tags=['Публикации']
    )
)
@method_decorator(
    name='destroy',
    decorator=swagger_auto_schema(
        operation_summary='Удалить публикацию',
        tags=['Публикации']
    )
)
class PublicationsViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all().order_by('-created')
    serializer_class = PublicationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['author', ]

    def perform_create(self, serializer):
        data = {
            'author': self.request.user
        }
        serializer.save(**data)


@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        operation_summary='Список комментариев к публикации',
        manual_parameters=[
            openapi.Parameter(
                'level',
                openapi.IN_QUERY,
                'Возвращает все комментарии до указанного уровня вложенности',
                type=openapi.TYPE_INTEGER
            )
        ],
        tags=['Комментарии']
    )
)
@method_decorator(
    name='create',
    decorator=swagger_auto_schema(
        operation_summary='Добавить комментарий к публикации',
        tags=['Комментарии']
    )
)
@method_decorator(
    name='update',
    decorator=swagger_auto_schema(
        operation_summary='Обновить комментарий к публикации',
        tags=['Комментарии']
    )
)
@method_decorator(
    name='partial_update',
    decorator=swagger_auto_schema(
        operation_summary='Обновить комментарий частично',
        tags=['Комментарии']
    )
)
@method_decorator(
    name='destroy',
    decorator=swagger_auto_schema(
        operation_summary='Удалить комментарий к публикации',
        tags=['Комментарии']
    )
)
class CommentsViewSet(
                mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                viewsets.GenericViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Comment.objects.none()
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

    @swagger_auto_schema(
        method='get',
        operation_summary='Детализация комментария, включая все вложенные',
        manual_parameters=[
            openapi.Parameter(
                'level',
                openapi.IN_QUERY,
                'Возвращает все комментарии к текущему комментарию \
                    до указанного уровня вложенности',
                type=openapi.TYPE_INTEGER
            )
        ],
        tags=['Комментарии']
    )
    @swagger_auto_schema(
        method='post',
        operation_summary='Добавление комментария, к другому комментарию',
        tags=['Комментарии']
    )
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
            publication_id=publication_id,
            id=pk
        )
        serializer = CommentSerializer(
            comment,
            context={
                'request': request
            }
        )
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
