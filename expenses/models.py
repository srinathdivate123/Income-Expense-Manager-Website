from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.
class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now) # By default it takes the current time
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=256)
    
    def __str__(self):
        return self.category

    class Meta:
        ordering: ['-date']  # The -ve sign infornt of date means that we will get the latest expenses on the top
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name