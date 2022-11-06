from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from .serializers import ProductSerializer, ProductDetailSerializer
from .models import Product
from .permissions import ReadOnlyOrAuthenticatedSeller, ReadOnlyOrProductOwner
from utils import SerializerByMethodMixin


class ProductView(SerializerByMethodMixin, ListCreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [ReadOnlyOrAuthenticatedSeller]
    serializer_map = {
        "GET": ProductSerializer,
        "POST": ProductDetailSerializer,
    }

    def perform_create(self, serializer):
        return serializer.save(seller=self.request.user)


product_view = ProductView.as_view()


class ProductDetailView(SerializerByMethodMixin, RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    permission_classes = [ReadOnlyOrProductOwner]
    lookup_url_kwarg = "product_id"
    serializer_map = {
        "GET": ProductDetailSerializer,
        "PATCH": ProductDetailSerializer,
    }


product_detail_view = ProductDetailView.as_view()
