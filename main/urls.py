from django.urls import path
from .views import (ClientAPIView, DragAndDropAPIView,
                     PayProductAPIView, ProductAPIView,
                       Login, Logout,
                         ProductSalesReport)

app_name="main"

urlpatterns = [
    path('clients/', ClientAPIView.as_view(), name='client-list'),
    path('drag_and_drop/', DragAndDropAPIView.as_view(), name='drag-and-drop'),
    path('pay_product/', PayProductAPIView.as_view(), name='pay-product'),
    path('products/', ProductAPIView.as_view(), name='product-list'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('sales_product_static/' , ProductSalesReport.as_view() , name="sales_product_static"),
]
