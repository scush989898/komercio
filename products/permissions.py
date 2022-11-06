from rest_framework.permissions import BasePermission
from rest_framework.views import Request, View

from products.models import Product


class ReadOnlyOrAuthenticatedSeller(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return (
            request.method == "GET"
            or request.user.is_authenticated
            and request.user.is_seller
        )


class ReadOnlyOrProductOwner(BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Product) -> bool:
        return (
            request.method == "GET"
            or request.user.is_authenticated
            and request.user == obj.seller
        )
