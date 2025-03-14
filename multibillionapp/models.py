from django.db import models

# Create your models here.
class  client(models.Model):
    fullname=models.CharField(max_length=100)
    age=models.IntegerField()
    email=models.EmailField()
    message=models.TextField()

    def __str__(self):
        return self.fullname

class contractor(models.Model):
    name=models.CharField(max_length=50)
    department=models.CharField(max_length=100)
    email=models.EmailField()
    age=models.IntegerField()
    qualification=models.CharField(max_length=50)

    def __str__(self):
        return self.name
class appointment(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=100)
    date=models.DateField()
    department=models.CharField(max_length=100)
    contractor=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Transaction(models.Model):
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=[('Success', 'Success'), ('Failed', 'Failed')])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.amount} - {self.status}"