from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
from django.contrib.auth import login, logout, authenticate
from django.utils.dateparse import parse_date
from django.db.models import Sum
from datetime import timedelta
from .models import *
from .serializers import *



   
class ClientAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = Client.objects.all()
        serializer = ClientSerializer(queryset, many=True)
        return Response(serializer.data ,status=status.HTTP_200_OK)

    def post(self, request):
        client_serializer = ClientSerializer(data=request.data)

        if client_serializer.is_valid():
            with transaction.atomic():
                client, created = Client.objects.get_or_create(**client_serializer.validated_data)
                drag_and_drop = DragAndDrop.objects.get(special_key="5a192310-fcaf-4961-86e6-1a171dafe373")
                drag_and_drop.clients.add(client)

            return Response(client_serializer.data, status=status.HTTP_201_CREATED)

        return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DragAndDropAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = self.get_data()
        serializer = DragAndDropSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            client_id, current_key, target_key = (
                request.data.get("client_id"),
                request.data.get("current_key"),
                request.data.get("target_key"),
            )

            with transaction.atomic():
                drag_and_drop_current = self.get_by_key(current_key)
                for d_current in drag_and_drop_current:
                    d_current.clients.remove(client_id)

                drag_and_drop_target = self.get_by_key(target_key)
                for d_target in drag_and_drop_target:
                    d_target.clients.add(client_id)

            return Response({"message": "Successful"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Error {e}"}, status=status.HTTP_404_NOT_FOUND)

    def get_data(self):
        return DragAndDrop.objects.all()

    def get_by_key(self, current_key):
        return DragAndDrop.objects.filter(special_key=f"{current_key}").prefetch_related('clients')

class PayProductAPIView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            queryset = PayProduct.objects.all()
            serializer = PayProductSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            name, product_id, quantity, = (
                request.data.get('name'),
                request.data.get('product_id'),
                request.data.get('quantity')
            )

            product = Product.objects.get(id=product_id)

            if product.quantity_on_hand < quantity:
                return Response({"error": "Not enough quantity in stock"}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                product.quantity_on_hand -= quantity
                product.save()

                sale = Sales.objects.create(product=product, quantity_sold=quantity)

                pay_product = PayProduct.objects.create(name=name, product=product, quantity=quantity)

            return Response({"message": "Sale and payment successful"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Error {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ProductAPIView(APIView):
    def get(self, request):
        try:
            queryset = Product.objects.all()
            serializer = ProductSerializer(queryset , many=True)
            return Response(serializer.data , status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error":f"Error {e}"} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
    def post(self, request):
        try:
            product_serializer = ProductSerializer(data=request.data)

            if product_serializer.is_valid():
                with transaction.atomic():
                    product_instance, created = Product.objects.get_or_create(**product_serializer.validated_data)

                if created:
                    return Response(product_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Product already exists"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": f"Error {e}"}, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def get(self , request):
        try:
            username, password = (
                request.data.get('username'),
                request.data.get('password')
            )
            user = authenticate(username=username, password=password)

        except Exception as e:
            return Response({"error":f"Error {e}"} , status=status.HTTP_404_NOT_FOUND)

class Logout(APIView):
    def get(self , request):
        try:
            logout(request)
            return Response({"message":"Successful"} , status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":f"Error {e}"}, status=status.HTTP_400_BAD_REQUEST)



class ProductSalesReport(APIView):
    def post(self, request):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        if not start_date or not end_date:
            return Response({"error": "Error: Start date or end date is missing."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
        except ValueError:
            return Response({"error": "Error: Date format is not recognized. Please send the date with the format YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        end_date = end_date + timedelta(days=1)

        product_sales = Sales.objects.filter(
            sale_date__range=[start_date, end_date]
        ).values('product__name').annotate(total_quantity_sold=Sum('quantity_sold'))

        response_data = [{"product_name": sale['product__name'], "total_quantity_sold": sale['total_quantity_sold']} for sale in product_sales]
        return Response(response_data)
