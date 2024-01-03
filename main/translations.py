from modeltranslation.translator import register, TranslationOptions
from .models import  DragAndDrop, Product, PaymentType



@register(DragAndDrop)
class DragAndDropTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name',)



@register(PaymentType)
class PaymentTypeTranslationOptions(TranslationOptions):
    fields = ('title',)
