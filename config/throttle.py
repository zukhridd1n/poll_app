from rest_framework.throttling import UserRateThrottle


class RoleBasedThrottle(UserRateThrottle):
    def custom_rate(self, request):
        # Check if the user is authenticated and an admin, and return the custom rate
        if request.user.is_authenticated and request.user.role == "admin":
            return "5/min"
        # Use the default rate if not an admin
        return super().get_rate()

    def allow_request(self, request, view):
        # Pass the request to the get_rate method
        self.rate = self.custom_rate(request)
        return super().allow_request(request, view)
