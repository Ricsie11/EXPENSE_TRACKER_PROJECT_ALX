import django_filters
from .models import Expense, Income

class ExpenseFilter(django_filters.FilterSet):
    date_min = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_max = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Expense
        fields = ['category', 'date_min', 'date_max']

class IncomeFilter(django_filters.FilterSet):
    date_min = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_max = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Income
        fields = ['category', 'date_min', 'date_max']
