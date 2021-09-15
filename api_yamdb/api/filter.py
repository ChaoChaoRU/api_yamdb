from django_filters import rest_framework as rest

from reviews.models import Title


class TitleFilter(rest.FilterSet):
<<<<<<< HEAD
    name = rest.CharFilter(field_name='name', lookup_expr='contains')
    category = rest.CharFilter(
        field_name='category__slug',
        lookup_expr='contains'
    )
    genre = rest.CharFilter(
        field_name='genre__slug',
        lookup_expr='contains'
=======
    name = rest.CharFilter(
        field_name='name',
        lookup_expr='contains'
    ),
    genre = rest.CharFilter(
        field_name='genre__slug',
        lookup_expr='contains'
    ),
    category = rest.CharFilter(
        field_name='category__slug',
        lookup_expr='contains'
>>>>>>> c9ee626fe0fe94b5419ff6ded6d5fd72240a0f67
    )

    class Meta:
        model = Title
        fields = ['name', 'genre', 'category', 'year']