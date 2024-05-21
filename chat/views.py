from django.shortcuts import render, redirect

def index(request):
    username = request.session.get('username')
    if not username:
        return redirect('chat:login')
    return render(request, 'chat/index.html', {'username': username})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        request.session['username'] = username
        return redirect('chat:room')
    return render(request, 'chat/login.html')