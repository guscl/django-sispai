from django.db import models
from django.contrib.auth.models import User

class Pool(models.Model):
    adult = models.OneToOneField(User)
    url = models.CharField(max_length=200)
    isActivated = models.BooleanField()
    infraRed = models.BooleanField()
    infraRedFail = models.BooleanField()
    zigbee = models.BooleanField()
    zigbeeFail = models.BooleanField()
    endCourseOpen = models.BooleanField()
    endCourseOpenFail = models.BooleanField()
    endCourseClose = models.BooleanField()
    endCourseCloseFail = models.BooleanField()
    crush = models.BooleanField()
    crushFail = models.BooleanField()
    def __str__(self):
    	return self.adult.username

class PoolLog(models.Model):
    pool = models.ForeignKey(Pool)
    time = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=500)
    @classmethod
    def create(cls,pool,message):
        log = cls(pool=pool,message=message)
        return log

