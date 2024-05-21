from django.db import models

# Create your models here.

class product(models.Model):
    CAT=((1,"shoes"),(2,"mobile"),(3,"cloths"))
    
    name=models.CharField(max_length=20,verbose_name="product name")
    price=models.IntegerField()
    cat=models.IntegerField(choices=CAT, verbose_name="category")
    pdetails=models.CharField(max_length=200, verbose_name="Details")
    is_active=models.BooleanField(default=True, verbose_name="Is_Available")
    pimage=models.ImageField(upload_to="image")

    def __str__(self):
        return self.name

class cart(models.Model):
    userid=models.ForeignKey('auth.user',on_delete=models.CASCADE,db_column='userid')
    pid=models.ForeignKey("product",on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)

class Order(models.Model):
    order_id=models.CharField(max_length=50)
    user_id=models.ForeignKey('auth.User',on_delete=models.CASCADE, db_column='userid')
    p_id=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)
    amt=models.FloatField()