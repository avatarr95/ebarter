from django.shortcuts import render
from django.views import generic
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Offer, OfferImage
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm, OfferCreateForm, AddOfferImageForm
from django.http import HttpResponseForbidden, Http404, HttpResponseRedirect
from django.contrib import messages
from django.forms import modelformset_factory, formset_factory
from django.urls import reverse_lazy
from django.template.defaultfilters import slugify
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index(request):
    special_offers = Offer.objects.filter(status="published", special=True)[:2]
    offers = Offer.objects.filter(status="published")
    return render(request, "bartapp/index.html", {'special_offers': special_offers, "offers": offers})
    

def offer_detail(request, pk, category, offer):
    offer = get_object_or_404(Offer, pk=pk, category=category, slug=offer)
    offer_images = offer.images.all()
    images = []
    for image in offer.images.all():
        try:
            images.append(image.image.url)
        except ValueError:
            continue

    return render(request, "bartapp/offer_detail.html", {"offer": offer, "images":images})

# 
# Creating a new user and adding him/her to a database
def register(request):
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, "bartapp/register_done.html", {'new_user': new_user})

    else:
        user_form = RegisterForm()
    return render (request, "bartapp/register.html", {'user_form': user_form})


@login_required
def profile(request, pk, username):
    user = get_object_or_404(User, pk=pk, username=username)
    return render(request, "bartapp/profile.html", {'user': user})

@login_required
def profile_edit(request, pk, username):
    user = get_object_or_404(User, pk=pk, username=username)
    profile = user.profile
    form = ProfileEditForm(request.POST or None, instance=profile)
    if request.user.username != user.username:
        return HttpResponseForbidden
    if form.is_valid():
        messages.success(request, "Twój profil został zaktualizowany pomyślnie")
        form.save()
        
    return render(request, "bartapp/profile_edit.html", {'user': user, "form":form})

def title_search(request):
    if request.method == "GET":
        title=request.GET.get('title')
        offers = Offer.objects.filter(title__icontains=title, status="published") 
        return render(request, "bartapp/search_results_name.html", {"offers": offers})
    else:
        return Http404

class CategorySearchView(generic.ListView):
    model=Offer
    def get_queryset(self):
        return Offer.objects.filter(category=self.kwargs['category'], status="published") 
    context_object_name="offers"
    template_name="bartapp/search_results.html"
    paginate_by = 3

class CitySearchView(generic.ListView):
    model=Offer
    def get_queryset(self):
        return Offer.objects.filter(localisation=self.kwargs['city'], status="published") 
    context_object_name="offers"
    template_name="bartapp/search_results.html"
    paginate_by = 3

@login_required
def create_offer(request):
    # ImageFormset = modelformset_factory(OfferImage, form=AddOfferImageForm, extra=7)
    ImageFormset = formset_factory(AddOfferImageForm, extra=7)
    if request.method == "POST":
        offer_form = OfferCreateForm(request.POST)
        image_formset = ImageFormset(request.POST, request.FILES)
        if offer_form.is_valid() and image_formset.is_valid():
            new_offer = offer_form.save(commit=False)
            new_offer.author = request.user
            new_offer.status = "draft"
            new_offer.slug = slugify(new_offer.title)
            new_offer.save()
            for form in image_formset.cleaned_data:
                image = form.get('image')
                new_image = OfferImage(offer=new_offer, image=image)
                new_image.save()
            return HttpResponseRedirect('/')
            
    else:
        offer_form = OfferCreateForm()
        image_formset = formset_factory(AddOfferImageForm, extra=7)
        return render(request, "bartapp/create_offer.html", {'offer_form': offer_form, "image_formset": image_formset})