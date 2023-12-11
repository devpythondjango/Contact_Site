from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.utils.decorators import method_decorator
from contact.models import Application, ApplicationCreate
from dashboard.models import Profile
from dashboard.forms import ProfileForm
from django.views import View


def login_decorator(func):
    return login_required(func, login_url='login')


def login_user(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, password=password, username=username)
        if user is not None:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'dashboard/login.html')


@login_decorator
def logout_user(request):
    logout(request)
    return redirect("login")


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfileView(View):
    profile = None

    def dispatch(self, request, *args, **kwargs):
        self.profile, __ = Profile.objects.get_or_create(user=request.user)
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {'profile': self.profile, 'segment': 'profile'}
        return render(request, 'dashboard/profile.html', context)

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=self.profile)
        if form.is_valid():
            profile = form.save()
            profile.user.first_name = form.cleaned_data.get('first_name')
            profile.user.last_name = form.cleaned_data.get('last_name')
            profile.user.email = form.cleaned_data.get('email')
            profile.user.save()

        return redirect('dashboard')


@login_decorator
def dashboard(request):
    app_count = Application.objects.count()
    app_status_yangi = ApplicationCreate.objects.filter(status='yangi').count()
    app_status_tekshirilmoqda = ApplicationCreate.objects.filter(status='tekshirilmoqda').count()
    app_status_tekshirildi = ApplicationCreate.objects.filter(status='tekshirildi').count()
    app_status_rad_etildi = ApplicationCreate.objects.filter(status='rad etildi').count()
    app_status_mal_topilmadi = ApplicationCreate.objects.filter(status='ma\'lumot topilmadi').count()
    ctx = {
        'app_count': app_count,
        'app_status_yangi': app_status_yangi,
        'app_status_tekshirilmoqda': app_status_tekshirilmoqda,
        'app_status_tekshirildi': app_status_tekshirildi,
        'app_status_rad_etildi': app_status_rad_etildi,
        'app_status_mal_topilmadi': app_status_mal_topilmadi,
    }
    return render(request, 'dashboard/index.html', ctx)