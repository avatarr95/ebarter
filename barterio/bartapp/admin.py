from django.contrib import admin
from .models import UserProfile, Offer, OfferImage
from sorl.thumbnail.admin import AdminImageMixin



class ImageInlines(AdminImageMixin, admin.TabularInline):
    model = OfferImage
    extra = 7
 

@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "mobile"]

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "date_published", "status")
    list_filter = ("date_published", "status")
    ordering = ("-updated", 'status')
    prepopulated_fields = {
        'slug': ('title',)
    }
    search_fields = ('title', 'author')

    inlines = [ImageInlines, ]

    