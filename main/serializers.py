from rest_framework import serializers
from .models import *



class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class DragAndDropSerializer(serializers.ModelSerializer):
    clients = ClientSerializer(many=True)

    class Meta:
        model = DragAndDrop
        fields = '__all__'



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'

class PayProductSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = PayProduct
        fields = '__all__'

class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
