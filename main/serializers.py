# serializers.py
from rest_framework import serializers
from modeltranslation.translator import TranslationOptions, register
from .models import *



@register(DragAndDrop)
class DragAndDropTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name',)




@register(PaymentType)
class PaymentTypeTranslationOptions(TranslationOptions):
    fields = ('title',)




class TranslatedFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model = self.Meta.model
        translations = model._meta.translations
        for lang_code, fields in translations.items():
            for field in fields:
                localized_field_name = f"{field}_{lang_code}"
                self.fields[localized_field_name] = serializers.CharField(source=localized_field_name, read_only=True)

    class Meta:
        abstract = True


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class DragAndDropSerializer(TranslatedFieldsModelSerializer):
    clients = ClientSerializer(many=True)

    class Meta:
        model = DragAndDrop
        fields = '__all__'


class ProductSerializer(TranslatedFieldsModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class SalesSerializer(TranslatedFieldsModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'


class PayProductSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = PayProduct
        fields = '__all__'


class PaymentTypeSerializer(TranslatedFieldsModelSerializer):
    class Meta:
        model = PaymentType
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
