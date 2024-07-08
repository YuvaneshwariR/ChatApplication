from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from django.shortcuts import render, HttpResponseRedirect, redirect

@api_view(["GET", "POST"])
def login_user(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        logout(request)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session["newvariable"] = "test"
                return HttpResponseRedirect("/api/find_people")
        return render(request, "login.html")


@api_view(["GET", "POST"])
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")