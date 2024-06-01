from django.db import models
from django.contrib.auth.models import User
import random
from django.db.models.signals import post_save
from django.dispatch import receiver


class KindOfInsurance(models.Model):
    description = models.CharField(max_length=100)
    
    def __str__(self):
        return self.description


class ReservedUsername(models.Model):
    username = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.username}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    additional_info = models.CharField(max_length=255, blank=True, null=True)
    assigned_color = models.CharField(max_length=20, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.assigned_color:
            colors = ['rgb(33, 122, 47)', 'rgb(181, 167, 226)', 'rgb(247, 115, 189)', 
                      'rgb(97, 81, 198)', 'rgb(204, 229, 207)', 'rgb(14, 51, 34)', 'rgb(215, 75, 11)', 
                      'rgb(40, 68, 215)', 'rgb(119, 130, 253)', 'rgb(98, 125, 96)', 'rgb(129, 217, 78)', 
                      'rgb(115, 107, 88)', 'rgb(61, 96, 162)', 'rgb(200, 117, 227)', 'rgb(250, 193, 99)', 
                      'rgb(100, 152, 63)', 'rgb(24, 115, 103)', 'rgb(38, 173, 24)', 'rgb(56, 32, 211)', 
                      'rgb(54, 208, 100)', 'rgb(40, 164, 173)', 'rgb(118, 135, 24)', 'rgb(71, 157, 213)', 
                      'rgb(62, 40, 200)', 'rgb(177, 208, 192)', 'rgb(239, 246, 90)', 'rgb(222, 145, 88)', 
                      'rgb(40, 230, 192)', 'rgb(205, 242, 172)', 'rgb(253, 187, 202)', 'rgb(62, 222, 5)', 
                      'rgb(72, 215, 185)', 'rgb(128, 78, 135)', 'rgb(158, 199, 202)', 'rgb(7, 41, 29)', 
                      'rgb(30, 51, 140)', 'rgb(24, 247, 193)', 'rgb(133, 203, 235)', 'rgb(221, 5, 128)', 
                      'rgb(14, 161, 37)', 'rgb(214, 0, 94)', 'rgb(24, 2, 134)', 'rgb(242, 201, 77)', 'rgb(1, 139, 44)',
                        'rgb(171, 196, 4)', 'rgb(78, 102, 210)', 'rgb(255, 156, 142)', 'rgb(247, 183, 202)', 
                        'rgb(68, 108, 212)', 'rgb(129, 146, 46)']
            self.assigned_color = random.choice(colors)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}"
      

class Customer(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code= models.CharField(max_length=20)
    assigned_color = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email} {self.phone} {self.address}"
    

class Insurance(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    kind_of_insurance = models.ForeignKey(KindOfInsurance, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    subject_of_insurance= models.CharField(max_length=100, null=True, blank=True)
    valid_from = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer.first_name} {self.kind_of_insurance} {self.amount} {self.subject_of_insurance} {self.valid_from} {self.valid_until}"

