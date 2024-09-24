from rest_framework.filters import SearchFilter


class PollSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        search_fields = ["question"]
        if request.query_params.get("username_only"):
            search_fields.append("author__username")
        if request.query_params.get("phone_only"):
            search_fields.append("author__phone")

        return search_fields
