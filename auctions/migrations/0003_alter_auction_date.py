# Generated by Django 4.0.3 on 2022-04-17 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_catogery_watchlist_comment_bid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
