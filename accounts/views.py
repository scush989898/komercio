from rest_framework.generics import (
    ListCreateAPIView,
    UpdateAPIView,
)
from .serializers import AccountSerializer
from .models import Account
from rest_framework.permissions import IsAdminUser
from .permissions import AccountOwner


class AccountView(ListCreateAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


acc_view = AccountView.as_view()


class AccountFilterNewestView(ListCreateAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def get_queryset(self):
        num = self.kwargs["num"]
        return self.queryset.order_by("date_joined").reverse()[:num]


acc_filter_newest_view = AccountFilterNewestView.as_view()


class AccountDetailView(UpdateAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    lookup_url_kwarg = "account_id"
    permission_classes = [AccountOwner]

    def update(self, request, *args, **kwargs):
        if request.user.is_superuser == False and "is_active" in request.data:
            request.data.pop("is_active")
        return super().update(request, *args, **kwargs)


acc_detail_view = AccountDetailView.as_view()


class AccountManagementView(UpdateAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    lookup_url_kwarg = "account_id"
    permission_classes = [IsAdminUser]


acc_management_view = AccountManagementView.as_view()
