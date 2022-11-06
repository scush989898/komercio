from django.urls import path
from .views import acc_filter_newest_view, acc_view, acc_detail_view, acc_management_view
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("login/", obtain_auth_token),
    path("accounts/", acc_view),
    path("accounts/newest/<int:num>/", acc_filter_newest_view),
    path("accounts/<account_id>/", acc_detail_view),
    path("accounts/<account_id>/management/", acc_management_view),
]
