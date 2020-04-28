from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
import datetime
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from django.urls import reverse
from sorl.thumbnail import ImageField


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    date_of_birth = models.DateField()
    mobile = PhoneNumberField(unique=True)
    company_name = models.CharField(max_length=50, blank=True)
    company_description = RichTextField(blank=True)
    company_short_description = models.CharField(max_length=120, blank=True)
    company_account = models.CharField(max_length=26, blank=True)
    localisation = models.CharField(max_length = 50)
    transfer_data = RichTextField(blank=True)

    @property
    def is_adult(self):
        return datetime.date.today() - self.date_of_birth > datetime.timedelta(6567)
    
    def __str__(self):
        return f"This is {self.user.username}'s profile"
    
    def get_absolute_url(self):
        return reverse("bartapp:profile", args=[self.user.pk, self.user.username])


class Offer(models.Model):
    CATEGORIES_CHOICES = (
        ('art_spoz', 'Artykuły spożywcze'),
        ('edukacja', 'Edukacja'),
        ('ogrodnictwo', 'Ogrodnictwo'),
        ('zdrowie_uroda', "Zdrowie i uroda"),
        ('uslugi', 'Usługi'),
        ('prawo', "Prawo"),
        ('odziez_obuwie', "Odzież i Obuwie"),
        ('inne', "Inne")
    )

    STATUS_CHOICES = (
        ('draft', "Draft"),
        ('published', "Published")
    )

    TRANSFER_CHOICES = (
        ('gotowka', "Gotówka"),
        ('przelew', 'Przelew'),
        ('wymiana', 'Wymiana'),
        ('wymiana_gotowka', 'Wymiana + gotówka'),
        ('wymiana_przelew', 'Wymiana + przelew')
    )


    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="offers")
    title = models.CharField(max_length=50)
    slug=models.SlugField()
    date_published = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    category = models.CharField(max_length=20, choices=CATEGORIES_CHOICES)
    description = RichTextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    estimated_value = models.DecimalField(decimal_places=2, max_digits=10)
    transfer = models.CharField(max_length=20, choices=TRANSFER_CHOICES)
    localisation = models.CharField(max_length=50, default='')
    special = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super(Offer, self).save(*args, **kwargs)
        self.slug = slugify(self.title)

    def get_absolute_url(self):
        return reverse("bartapp:offer_detail", args=[self.pk, self.category, self.slug])

    @property
    def has_max_photos(self):
        return self.images.count() >= 8

    class Meta:
        ordering = ('-date_published', )

class OfferImage(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="images")
    image = ImageField(upload_to="images/%Y/%m/%d", blank=True)

    def __str__(self):
        return self.offer.title