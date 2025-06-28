from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login

User = get_user_model()

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Barcha maydonlarni to‘ldiring.")
            return redirect('/auth/register/')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu username allaqachon mavjud.")
            return redirect('/auth/register/')

        User.objects.create_user(username=username, password=password)
        return redirect('/auth/login/')



class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Login yoki parol noto‘g‘ri.")
            return redirect('login_page')
