from rest_framework import viewsets

from .models import Publication
from .serializers import PublicationSerializer


class PublicationsViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all().order_by('-pub_date')
    serializer_class = PublicationSerializer
