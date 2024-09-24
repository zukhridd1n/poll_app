from rest_framework.filters import OrderingFilter


class ChoiceOrderingFilter(OrderingFilter):

    def filter_queryset(self, request, queryset, view):
        ordering = request.query_params.get(self.ordering_param)

        if "poll_author_id" in ordering:
            return queryset.order_by("poll__author_id")

        return super().filter_queryset(request, queryset, view)
