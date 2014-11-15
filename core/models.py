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
    isOpen = models.BooleanField()
    def __str__(self):
    	return self.adult.email

class PoolLog(models.Model):
    pool = models.ForeignKey(Pool)
    time = models.DateField(auto_now=True)
    message = models.CharField(max_length=500)
    @classmethod
    def create(cls,pool,message):
        book = cls(pool=pool,message=message)
        # do something with the book
        return log