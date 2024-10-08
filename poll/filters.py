from rest_framework.filters import BaseFilterBackend


class AnswerFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        answer = request.query_params.get('answer', None)
        if answer:
            queryset.filter(answer__iendswith=f'{answer}')

        return queryset