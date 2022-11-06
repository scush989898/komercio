from rest_framework.urls import path
from .views import product_view, product_detail_view

urlpatterns = [
    path("products/", product_view),
    path("products/<product_id>/", product_detail_view),
]
