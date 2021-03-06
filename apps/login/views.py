from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.core.urlresolvers import reverse

def index(request):
    try:
        request.session['logged_in']
        return redirect(reverse('login_home', kwargs={'id':request.session['logged_in']}))
    except KeyError:
        return render(request, 'login/index.html')

def login(request):
    if request.method == "POST":
        results = User.userManager.ValidLogin(request.POST)
        if results[0]:
            passFlag = True
            if 'logged_in' not in request.session:
                username = request.POST['username']
                request.session['logged_in'] = User.objects.get(username=username).id
                return redirect(reverse('login_home', kwargs={'id':request.session['logged_in']}))
        else:
            passFlag = False
            errors = results[1]
            for error in errors:
                messages.error(request, error)
            return redirect(reverse('login_index'))
    else:
        return redirect(reverse('login_index'))

def register(request):
    try:
        request.session['logged_in']
        return redirect(reverse('login_home', kwargs={'id':request.session['logged_in']}))
    except KeyError:
        return render(request, 'login/register.html')

# this part processes the submitted registration
def registration(request):
    if request.method == "POST":
        results = User.userManager.isValidRegistration(request.POST)
        if results[0]:
    		return redirect(reverse('login_index'))
        else:
        	errors = results[1]
        	for error in errors:
                    messages.error(request, error)
                return redirect(reverse('login_register'))
    else:
        return redirect(reverse('login_register'))

def logout(request):
	request.session.clear()
	return redirect (reverse('login_index'))
