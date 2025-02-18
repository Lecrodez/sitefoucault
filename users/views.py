from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

# from users.forms import UserForm


# def login_user(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно зарегистрированы!')
#             return redirect('login')  # Перенаправление на страницу входа
#     else:
#         form = UserForm()
#     return render(request, 'login.html', {'form': form})

def login_user(request):
    return HttpResponse("login")

def logout_user(request):
    return HttpResponse("logout")
