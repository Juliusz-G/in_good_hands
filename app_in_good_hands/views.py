
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
from .forms import LoginForm, RegisterForm, ProfileEditForm, UpdatePasswordForm

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


class Login(LoginView):
    """Login user. If form is invalid (username=email not in db) redirect to registration."""
    template_name = 'login.html'
    extra_context = {'form': LoginForm}


class Logout(LogoutView):
    """Logout user and redirect to Lading Page."""
    template_name = 'index.html'


class Register(CreateView):
    """Sends an activation link on email, if confirmed saves new user to db."""
    model = User
    form_class = RegisterForm
    template_name = 'register.html'

    def form_valid(self, form):
        """if form is valid, saves user and sends email"""
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Link aktywacyjny twojego konta.'
        message = render_to_string('register_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = form.cleaned_data.get('username')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('Wysłaliśmy link aktywacyjny na twojego maila. Prosze odczytać wiadomość i kliknąć w link.')


def activate(request, uidb64, token):
    """Builds up and activation link and makes user active if link was clicked."""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Dziękujemy za aktywowanie konta. Możesz się teraz zalogować.')
    else:
        return HttpResponse('Link aktywacyjny niepoprawny!')


class Profile(TemplateView):
    """Displays user info."""
    template_name = 'profile.html'

    def get_context_data(self, user_id):
        """Passes data to page."""
        user = User.objects.get(pk=user_id)
        donations = Donation.objects.filter(user=self.request.user).order_by("pk")

        ctx = {
            'user': user,
            'donations': donations
        }

        return ctx


class ProfileEdit(UpdateView):
    """Shows profile edit form with password confirmation."""
    model = User
    form_class = ProfileEditForm
    template_name = 'profile_edit.html'
    success_url = '/'

    def get_object(self, queryset=None):
        """Returns logged user object."""
        return self.request.user


class UpdatePassword(UpdateView):
    """Allows user to change password. Logs out user after submit a form."""
    form_class = UpdatePasswordForm
    template_name = 'change_password.html'
    success_url = '/'

    def get_object(self, queryset=None):
        """Returns logged user object."""
        return self.request.user
