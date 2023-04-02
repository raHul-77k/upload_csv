from django.db import models

class Transaction(models.Model):
    invoice_id = models.CharField(max_length=100)
    product_line = models.CharField(max_length=100)
    unit_price = models.FloatField()
    quantity = models.IntegerField()
    tax = models.FloatField()
    total = models.FloatField()
    date = models.DateField()
    time = models.TimeField()