import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Catogery(models.Model):
    catogery=models.CharField(max_length=225)

    def __str__(self):
        return f'{self.catogery}'

    class Meta:
        verbose_name = 'Catogery'
        verbose_name_plural = 'Catogeries'


class Auction (models.Model):
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=225)
    imgurl = models.URLField(max_length=200)
    date = models.DateTimeField()
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    catogery = models.ForeignKey(Catogery,on_delete=models.CASCADE)
    active=models.BooleanField(default=True)
    start_bid=models.IntegerField(default=0)
    last_bid=models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name='Auction'
        verbose_name_plural='Auctions'


class Bid (models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    auctions=models.ForeignKey(Auction,on_delete=models.CASCADE)
    bid=models.IntegerField()
    def __str__(self):
        return f'{self.auctions}: {self.bid} bids'

    class Meta:
        verbose_name='Bid'
        verbose_name_plural='Bids'


class Comment (models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comments=models.CharField(max_length=255)
    auctions=models.ForeignKey(Auction,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}:  comments'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class WatchList(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    auctions=models.ForeignKey(Auction,on_delete=models.CASCADE,blank=True)

    def __str__(self):
        return f'{self.user}: whichList'

    class Meta:
        verbose_name = 'WatchList'
        verbose_name_plural = 'WatchLists'