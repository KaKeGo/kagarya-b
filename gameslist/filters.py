from django_filters import rest_framework as filters
from django.db.models import Q

from .models import (
    GameList, Category
)


class GameListFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    category = filters.CharFilter(method='filter_category')

    class Meta:
        model = GameList
        fields = [
                'title', 'category'
            ]
    def filter_category(self, queryset, name, value):
        categories = value.split('&')
        for category in categories:
            queryset = queryset.filter(category__name__icontains=category.strip())
        return queryset
