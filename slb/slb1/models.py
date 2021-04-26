from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Equipments(models.Model):
    name = models.CharField(max_length=300, null=True)
    discription = models.CharField(max_length=200, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    available = models.IntegerField(default=0, null=True, blank=True)
    borrowed = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    image = models.ImageField(default="yes1.jpg", null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
            return url


class Students(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    idn = models.CharField(max_length=200, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

class Reserve(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, null=True, blank=True)
    date_reserved = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)
    collect = models.BooleanField(default=False)
    approved =models.BooleanField(default=False)

    @property
    def get_reserved_items(self):
        reserveitems = self.reserveitem_set.all()
        total = sum([item.quantity for item in reserveitems])
        return total

    @property
    def get_reserved_total(self):
        reserveitems = self.reserveitem_set.all()
        total = sum([item.get_total for item in reserveitems])
        return total
 
class ReserveItem(models.Model):
    equipment = models.ForeignKey(Equipments, on_delete=models.CASCADE, null= True, blank= True)
    reserve = models.ForeignKey(Reserve, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


    @property
    def get_total(self):
        total = self.quantity
        return total