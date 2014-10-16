from django.db import models

class Adult(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=10)
    

class Pool(models.Model):
    adultEmail = models.ForeignKey(Adult)
    url = models.CharField(max_length=200)
    isActivated = models.BooleanField()
    isChecked = models.BooleanField()
    