from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "bartapp"

urlpatterns = [
    path('', views.index, name="index"),
    path("register/", views.register, name="register"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('<int:pk>/<slug:category>/<slug:offer>/', views.offer_detail, name="offer_detail"),
    path('user_profile/<int:pk>/<slug:username>/', views.profile, name="profile"),
    path('user_profile/<int:pk>/<slug:username>/edit/', views.profile_edit, name="profile_edit"),
    path('title_search_results/', views.title_search, name="title_search_results"),
    path('category_search_results/<str:category>/', views.CategorySearchView.as_view(), name="category_search_results"),
    path('city_search_results/<str:city>/', views.CitySearchView.as_view(), name="city_search_results"),
    path('create_offer/', views.create_offer, name="create_offer"),
]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)