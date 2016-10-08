from django.db import models
from django.contrib.postgres.fields import DateTimeRangeField
# from django.db.models import SET_NULL
from django.contrib.auth.models import User
from app.constants import TRANSACTION_STATES


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    address = models.CharField(max_length=1024)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return unicode(self.id)


class Owner(UserProfile):
    insurance = models.CharField(max_length=1024)

    def __unicode__(self):
        return unicode(self.id)


class Renter(UserProfile):
    field = models.CharField(max_length=1024)

    def __unicode__(self):
        return unicode(self.id)


class Car(models.Model):
    owner = models.ForeignKey(Owner)
    name = models.CharField(max_length=1024)
    price = models.IntegerField(default=30)
    short_description = models.CharField(max_length=200, default='short_description')
    description = models.CharField(max_length=5048)
    manufacture = models.IntegerField(default=2000)

    def __unicode__(self):
        return unicode(self.id)


class Transaction(models.Model):
    owner = models.ForeignKey(Owner)
    renter = models.ForeignKey(Renter)
    state = models.CharField(choices=TRANSACTION_STATES, default='0', max_length=64)

    def __unicode__(self):
        return unicode(self.id)
