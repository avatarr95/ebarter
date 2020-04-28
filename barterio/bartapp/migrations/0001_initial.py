# Generated by Django 3.0.5 on 2020-04-26 06:29

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('date_published', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('category', models.CharField(choices=[('zywnosc', 'Żywność'), ('edukacja', 'Edukacja'), ('ogrodnictwo', 'Ogrodnictwo'), ('zdrowie_uroda', 'Zdrowie i uroda'), ('uslugi', 'Usługi'), ('prawo', 'Prawo'), ('odziez_obuwie', 'Odzież i Obuwie'), ('inne', 'Inne')], max_length=20)),
                ('description', ckeditor.fields.RichTextField()),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], max_length=20)),
                ('estimated_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transfer', models.CharField(choices=[('gotowka', 'Gotówka'), ('przelew', 'Przelew'), ('wymiana', 'Wymiana'), ('wymiana_gotowka', 'Wymiana + gotówka'), ('wymiana_przelew', 'Wymiana + przelew')], max_length=20)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('mobile', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('company_name', models.CharField(blank=True, max_length=50)),
                ('company_description', ckeditor.fields.RichTextField(blank=True)),
                ('company_short_description', models.CharField(blank=True, max_length=120)),
                ('company_account', models.CharField(blank=True, max_length=26)),
                ('localisation', models.CharField(max_length=50)),
                ('transfer_data', ckeditor.fields.RichTextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OfferImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='images/%Y/%m/%d')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='bartapp.Offer')),
            ],
        ),
    ]
