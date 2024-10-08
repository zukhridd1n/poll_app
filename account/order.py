from rest_framework.filters import OrderingFilter


class CustomOrderingFilter(OrderingFilter):

    def filter_queryset(self, request, queryset, view):
        ordering = request.query_params.get(self.ordering_param)

        if 'plt' in ordering:
            return queryset.order_by('profile__passport_letter')

        return super().filter_queryset(request, queryset, view)
