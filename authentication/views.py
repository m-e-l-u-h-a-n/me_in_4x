from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from .forms import SignUpForm,LoginForm
from .tokens import account_activation_token
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .utils import send_email
def home(request):
    return render(request, 'home.html')

# @login_required
def logoutView(request,next_page):
    logout(request)
    return redirect('home')


def signup(request):

    if(request.method == 'POST'):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Verify Your Email"
            context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
            message = render_to_string(
                'account_activation_email.html', context)
            message = '<p>'+message+'</p>'
            #user.email_user(subject, message)
            send_email(user.email, subject, message)
            # set redirection url
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')

def loginView(request):
    if request.user.is_authenticated:
        print(request.user.username)
        return redirect('home')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid() and form.verify_credentials_and_login_user(request):
            return redirect('home')
        else:
            form = LoginForm()
    return render(request,'login.html',{'form':form})

