from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.viewsets import ModelViewSet

from core.models import Car
from core.serializers import CarSerializer


class MyPagination(CursorPagination):
    page_size = 15
    ordering = 'id'


class CarViewSet(ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    pagination_class = MyPagination

    def filter_queryset(self, queryset):
        for k, v in self.request.query_params.items():
            if k == 'cursor':
                continue
            queryset = queryset.filter(**{k: v})
        return queryset
