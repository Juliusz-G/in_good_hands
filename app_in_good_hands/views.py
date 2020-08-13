
# Django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView

# local Django
from .models import Category, Donation, Institution, User

# Create your views here.


class LandingPage(TemplateView):
    """Shows content (sum of donated bags and sum of all institutions) on Landing Page."""
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        """Context data of Landing Page."""
        institutions_sum = Institution.objects.count()
        bags_sum = Donation.objects.aggregate(Sum('quantity'))['quantity__sum']
        foundations = Institution.objects.filter(type=1)
        organizations = Institution.objects.filter(type=2)
        local_collections = Institution.objects.filter(type=3)

        if bags_sum is None:
            bags_sum = 0

        ctx = {
            'institutions_sum': institutions_sum,
            'bags_sum': bags_sum,
            'foundations': foundations,
            'organizations': organizations,
            'local_collections': local_collections,
        }
        return ctx