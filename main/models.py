from django.db import models
import random
import uuid 

def generate_shtrix():
    letters = [chr(random.randint(65, 90)) for _ in range(2)]  
    numbers = [str(random.randint(0, 9)) for _ in range(6)]  

    passport_series = ''.join(letters + numbers)
    return passport_series


class Client(models.Model):
    name = models.CharField(verbose_name="Name", max_length=25, help_text="Enter the client's name.")
    surname = models.CharField(verbose_name="Surname", max_length=25, help_text="Enter the client's surname.")
    phone_number = models.CharField(verbose_name="Phone Number", max_length=150, help_text="Enter the client's phone number.")
    reg_date = models.DateField(auto_now_add=True, verbose_name="Registration Date")

    def __str__(self):
        return f"{self.name} {self.surname} | Phone: {self.phone_number} | Registered on: {self.reg_date}"

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"


class DragAndDrop(models.Model):
    title = models.CharField(verbose_name="Title", max_length=150, help_text="Enter the request title.")
    clients = models.ManyToManyField(Client, verbose_name="Client", help_text="Select clients", blank=True)
    special_key = models.UUIDField(verbose_name="Special key:", default=uuid.uuid4, unique=True)
    reg_date = models.DateField(auto_now_add=True, verbose_name="Registration Date")

    def __str__(self):
        return f"{self.title} | Registered on: {self.reg_date} | Special Key: {self.special_key}"

    class Meta:
        verbose_name = "Drag And Drop"
        verbose_name_plural = "Drag And Drops"


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Product Name", help_text="Enter the product name.")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price", help_text="Enter the product price.")
    quantity_on_hand = models.IntegerField(default=0, verbose_name="Quantity on Hand", help_text="Enter the quantity on hand.")
    shtrix = models.CharField(verbose_name="Product Shtrix", max_length=150, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.shtrix:
            self.shtrix = generate_shtrix()
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} | Price: {self.price} | Quantity on Hand: {self.quantity_on_hand} | Shtrix: {self.shtrix}"

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product", help_text="Select product")
    quantity_sold = models.IntegerField(verbose_name="Quantity Sold", help_text="Enter the quantity sold.")
    sale_date = models.DateTimeField(auto_now_add=True, verbose_name="Sale Date")

    def __str__(self):
        return f"{self.product.name} | Quantity Sold: {self.quantity_sold} | Sale Date: {self.sale_date}"

    class Meta:
        verbose_name = "Sale"
        verbose_name_plural = "Sales"


class PayProduct(models.Model):
    name = models.CharField(max_length=25, verbose_name="Client Name", help_text="Enter the client's name.")
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE, help_text="Select product")
    quantity = models.IntegerField(verbose_name="Quantity", default=0, help_text="Enter the quantity.")
    price = models.IntegerField(verbose_name="Price", default=0, help_text="Enter the price.")
    pay_date = models.DateField(auto_now_add=True, verbose_name="Payment Date")
    id_payment = models.CharField(unique=True, max_length=150 ,help_text="Unique ID for the payment", verbose_name="ID Payment", blank=True)

    def save(self, *args, **kwargs):
        if not self.id_payment:
            self.id_payment = generate_shtrix()
        if self.product:
            self.price = self.quantity * self.product.price 

        super(PayProduct, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id_payment} | {self.name} | {self.product} | Quantity: {self.quantity} | Price: {self.price} | Payment Date: {self.pay_date}"

    class Meta:
        verbose_name = "Pay Product"
        verbose_name_plural = "Pay Products"




class Expense(models.Model):
    name = models.CharField(verbose_name="Client Name", max_length=150, help_text="Enter the client's name.")
    amount = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Amount", help_text="Enter the payment amount.")
    id_payment = models.CharField(verbose_name="ID Payment", max_length=150, blank=True, unique=True, help_text="Unique ID for the payment")
    reg_date = models.DateField(auto_now_add=True, verbose_name="Registration Date")

    def save(self, *args, **kwargs):
        if not self.id_payment:
            self.id_payment = generate_shtrix()
        super(Expense, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id_payment} | {self.name} | Payment Type: {self.payment_type.title} | Amount: {self.amount} | Registered on: {self.reg_date}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
