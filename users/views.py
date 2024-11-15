from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from users.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages

@csrf_exempt
def signup(request):
    if request.method == "GET":
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        role = request.POST.get('role')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # 验证密码是否一致
        if password != confirm_password:
            messages.error(request, "密码和确认密码不一致")
            return redirect('signup')

        # 创建用户
        user = User(username=username, email=email, phone=phone, gender=gender, role=role)
        user.set_password(password)  # 设置密码
        user.save()  # 保存用户

        # 登录用户
        login(request, user)

        messages.success(request, "注册成功！")
        return redirect('signin')  # 注册成功后重定向到主页
    return render(request, 'users/signup.html')





@csrf_exempt
def signin(request):
    form = AuthenticationForm()
    if request.method == "POST":
        return_form = AuthenticationForm(data=request.POST)
        if return_form.is_valid():
            user = return_form.get_user()
            login(request, user)
            next_url = request.POST.get('next', '/')
            return redirect(next_url)
    next_url = request.GET.get('next', '/')
    return render(request, 'signin.html', {'form': form, 'next': next_url})

@csrf_exempt
def signout(request):
    logout(request)
    return redirect('/')
