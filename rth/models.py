from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.db.models import   Avg
from chat.models import Profile
TRUE_FALSE=(
    ("True","True"),
    ("False","False"),
)

class Products(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    productName	= models.CharField(max_length=250)
    photo=models.ImageField(upload_to=f'product/{timezone.datetime.now().date()}')
    description = models.TextField(max_length=1000)
    price=models.DecimalField(max_digits=8, decimal_places=2)
    qty=models.IntegerField(default=1)
    
    @property
    def ratings(self):
        mean_of_ratings=Review.objects.filter(product=self).aggregate(Avg('stars'))['stars__avg']
        return mean_of_ratings
    @property
    def selleraccount(self):
        return Profile.objects.get(user=self.seller)
    
    def __str__(self):
        return f"{self.seller} - Products {self.productName}"

class Review(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE
                           )
    product=models.ForeignKey(Products, on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    body=models.TextField()
    stars=models.IntegerField()

    def __str__(self):
        return f"{self.title} {self.stars}"
    
class Cart(models.Model):
    cartcookie=models.CharField(max_length=100)
    product=models.ForeignKey(Products, on_delete=models.CASCADE)
    qty=models.IntegerField(default=1)
    checked=models.CharField(max_length=10, choices=TRUE_FALSE, default='False')


    def __str__(self):
        return f"Cart {self.cartcookie}"


class Order(models.Model):
    merchant_request_id = models.CharField(max_length=50)
    checkout_request_id = models.CharField(max_length=50)
    seller=models.ForeignKey(User,related_name='seller', on_delete=models.CASCADE)
    buyer=models.ForeignKey(User,related_name='buyer', on_delete=models.CASCADE)
    products=models.ForeignKey(Products, on_delete=models.CASCADE)
    qty=models.IntegerField(default=1)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    date=models.DateTimeField(default=timezone.now)
    order_status=models.CharField(max_length=10, choices=TRUE_FALSE, default='False')
    payment_status=models.CharField(max_length=10, choices=TRUE_FALSE, default='False')
    location=models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.seller} - {self.products}"

class MpesaPayment(models.Model):
    merchant_request_id = models.CharField(max_length=50)
    checkout_request_id = models.CharField(max_length=50)
    result_code = models.IntegerField()
    result_desc = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mpesa_receipt_number = models.CharField(max_length=50)
    transaction_date = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.mpesa_receipt_number} - Date: {self.transaction_date} - Phone: {self.phone_number} Amount Ksh. {self.amount}"
