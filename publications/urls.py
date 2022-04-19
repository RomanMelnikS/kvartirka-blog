from django.urls import include, path
from drf_yasg.utils import swagger_auto_schema
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import CommentsViewSet, PublicationsViewSet


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_summary='Создание токена.',
        tags=['Аутенфикация']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_summary='Обновление токена.',
        tags=['Аутенфикация']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


router_v1 = DefaultRouter()
router_v1.register(
    r'publications',
    PublicationsViewSet,
    basename='publications'
)
router_v1.register(
    r'publications/(?P<publication_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path(
        r'v1/',
        include(router_v1.urls)
    ),
    path(
        r'v1/users/token/login/',
        DecoratedTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        r'v1/users/token/refresh/',
        DecoratedTokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
