from django_filters import filters

from apps.shifts.models import Shift


class ShiftFilter(filters.FilterSet):
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
            'date_start_lte', 'date_start_gte', 'date_end_lte',
            'date_end_gte', )
