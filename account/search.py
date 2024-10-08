from rest_framework.filters import SearchFilter

class CustomSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('username_only'):
            return ['username']
        if request.query_params.get('email_only'):
            return ['email']
        return super().get_search_fields(view, request)

