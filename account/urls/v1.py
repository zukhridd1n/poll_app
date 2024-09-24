from django.urls import include, path
from rest_framework.routers import DefaultRouter

from account.views import (AccountView, GroupViewSet, InterestView,
                           PermissionViewSet)

router = DefaultRouter()
router.register("interest", InterestView, basename="interest")
router.register("permission", PermissionViewSet, basename="permission")
router.register("group", GroupViewSet, basename="group")
router.register("", AccountView, basename="account")
app_name = "account"
urlpatterns = [
    path("", include(router.urls)),
    # path('interest/', InterestView.as_view({"get":'list'})),
]
