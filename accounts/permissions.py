from rest_framework.permissions import BasePermission
from rest_framework.views import Request, View
from accounts.models import Account


class AccountOwner(BasePermission):
    def has_object_permission(
        self, request: Request, view: View, account: Account
    ) -> bool:
        return request.user == account
