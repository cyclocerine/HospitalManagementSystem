from django.db import models
from .supplier import Supplier

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    medicine_class = models.CharField(max_length=50)  # gol_obat
    medicine_type = models.CharField(max_length=50)   # jenis_obat
    expiry_date = models.DateField()
    stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name