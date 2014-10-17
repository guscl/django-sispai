from django.db import models

class Adult(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(primary_key = True,max_length=200)
    password = models.CharField(max_length=10)
    def __str__(self):
    	return self.name
    

class Pool(models.Model):
    adult = models.ForeignKey(Adult)
    url = models.CharField(max_length=200)
    isActivated = models.BooleanField()
    isChecked = models.BooleanField()
    def __str__(self):
    	return self.adultEmail.email
    