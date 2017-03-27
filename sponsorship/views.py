from django.shortcuts import render
from forms import LoginForm
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

def url_redirect(request):
    return HttpResponseRedirect('/sponsorship/')


def sponsorship_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.data['username'], password=form.data['password'])
            if user:
                # Is the account active? It could have been disabled.
                if user.is_active:
                    # If the account is valid and active, we can log the user in.
                    # We'll send the user back to the homepage.
                    login(request, user)
                    if user.is_staff or user.is_superuser:
                        return HttpResponseRedirect('/admin')
                    else:
                        raise Http404("That user not found")

                else:
                    # An inactive account was used - no logging in!
                    return HttpResponse("Sorry, this sponsorship account has been disabled.")
            else:
                # Bad login details were provided. So we can't log the user in.
                print("Invalid login details: {0}, {1}".format(form.data['username'], form.data['password']))
                return HttpResponse("Invalid login details supplied.")
    else:
        if request.user.is_authenticated():
            logout(request)
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def sponsorship(request):
    return render(request, 'sponsorship.html')
