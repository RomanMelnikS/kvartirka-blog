from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import PublicationsViewSet, CommentsViewSet

router_v1 = DefaultRouter()
router_v1.register(
    r'publications',
    PublicationsViewSet,
    basename='publications'
)
router_v1.register(
    r'publications/(?P<publication_id>\d+)/comments/',
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
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        r'v1/users/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
