from django_filters import filters, FilterSet

from apps.shifts.models import Shift


class ShiftFilter(FilterSet):
    date_start__lte = filters.DateFilter(
        name='date_start',
        lookup_expr='date__lte'
    )
    date_start__gte = filters.DateFilter(
        name='date_start',
        lookup_expr='date__gte'
    )
    date_end__lte = filters.DateFilter(
        name='date_end',
        lookup_expr='date__lte'
    )
    date_end__gte = filters.DateFilter(
        name='date_end',
        lookup_expr='date__gte'
    )

    class Meta:
        model = Shift
        fields = (
            'date_start__lte', 'date_start__gte', 'date_end__lte',
            'date_end__gte', )
