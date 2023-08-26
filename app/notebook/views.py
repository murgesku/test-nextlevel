from django.db.models import Value as V, F
from django.db.models.functions import Concat
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from .models import *
from .serializers import *


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().annotate(full_name=Concat(F('first_name'), V(' '), F('last_name')))
    serializer_class = ContactSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'full_name']

    permission_classes = [permissions.IsAuthenticated]
