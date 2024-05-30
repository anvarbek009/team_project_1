from django.db import models

# Create your models here.

class Admin(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,blank=True, null=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=100,blank=True, null=True)
    image = models.ImageField(upload_to='admin_image/',blank=True, null=True)

    class Meta:
        db_table = 'admin'

    def __str__(self):
        return self.name