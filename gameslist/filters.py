import django_filters

from .models import GameList


class GameListFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = GameList
        fields = [
                'title',
            ]
