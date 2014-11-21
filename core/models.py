from django.db import models
from django.contrib.auth.models import User

class Pool(models.Model):
    adult = models.OneToOneField(User)
    url = models.CharField(max_length=200)
    isActivated = models.BooleanField()
    isChecked = models.BooleanField()
    isOpen = models.BooleanField()
    def __str__(self):
    	return self.adult.username

class PoolLog(models.Model):
    pool = models.ForeignKey(Pool)
    time = models.DateField(auto_now=True)
    message = models.CharField(max_length=500)
    @classmethod
    def create(cls,pool,message):
        book = cls(pool=pool,message=message)
        # do something with the book
        return log
