from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from .forms import UserSignupForm, WriterCreateForm


# Create your views here.
def landing_page(request):
    return render(request, 'landing.html')


def register(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            new_user = form.save(commit=False)
            new_user.set_password(form_data.get('password'))
            new_user.save()
            if form.cleaned_data.get('account_type') == 'reader':
                return render(request, 'registration/login.html')
            else:
                user = authenticate(request, username=form_data.get('username'), password=form_data.get('password'))
                login(request, user)
                return redirect('register_as_writer')
        else:
            return render(request, 'register.html', {'form':form})
    else:
        form = UserSignupForm()
        return render(request, 'register.html', {'form':form})

def login_redriect(request):
    return render(request, 'login_redirect.html')


@login_required
def register_writer(request):
    if request.method == 'POST':
        form = WriterCreateForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            logout(request)
            return redirect('login')
        else:
            return render(request, 'writer_profile_creation_form.html', {'form':form})
    else:
        form = WriterCreateForm()
        return render(request, 'writer_profile_creation_form.html',{'form':form} )
            
