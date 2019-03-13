from django.shortcuts import render

# Create your views here.

from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm
from django.contrib.auth.backends import ModelBackend

from .models import UserProfile
from article.models import Article
from organization.models import Department


# 重載Django的賬號密碼驗證方法
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(username=username)
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class loginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html", {"username": user})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误！"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class logoutView(View):
    def get(self, request):
        logout(request)
        return render(request, "index.html", {})


class IndexView(View):
    def get(self, request):
        article = Article.objects.all()
        num = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
        departmentList = Department.objects.all()
        return render(request, "index.html",
                      context={"articleList": article, "num": num, "departmentList": departmentList})


def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
