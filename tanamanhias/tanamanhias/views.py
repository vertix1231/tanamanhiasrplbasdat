from django.shortcuts import render, redirect


from django.contrib.auth import authenticate, login, logout


def index(request):
     context = {
          'title':'Orplant',

     }
     return render(request, 'index.html', context)


def loginView(request):
    context = {
              'title':'Orplant',

     }

    user = None
    if request.method == "GET":
        if request.user.is_authenticated():
            return redirect('index')
        else:
            return render(request, 'login.html', context)

    if request.method == "POST":
        username_login = request.POST['username']
        password_login = request.POST['password']
        print(username_login)
        user = authenticate(request, username = username_login, password = password_login)
        print(user, 'ini user nya ')
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return redirect('login')
    print("masuk")
    return render(request, 'login.html', context)


