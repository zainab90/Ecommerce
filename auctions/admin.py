from django.contrib import admin

# Register your models here.
from auctions.models import Auction, AbstractUser, Comment, Bid,Catogery, WatchList

admin.site.register(Auction)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Catogery)
admin.site.register(WatchList)

