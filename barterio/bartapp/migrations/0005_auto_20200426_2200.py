# Generated by Django 3.0.5 on 2020-04-26 20:00

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bartapp', '0004_offer_special'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offerimage',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, upload_to='images/%Y/%m/%d'),
        ),
    ]