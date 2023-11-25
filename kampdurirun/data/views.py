from django.shortcuts import render, get_object_or_404, redirect
from .models import UserData
from .forms import UserDataForm

def show_user_data(request):
    user_data = get_object_or_404(UserData, user=request.user)
    return render(request, 'show_user_data.html', {'user_data': user_data})

def edit_user_data(request):
    user_data = get_object_or_404(UserData, user=request.user)

    if request.method == 'POST':
        form = UserDataForm(request.POST, instance=user_data)
        if form.is_valid():
            form.save()
            return redirect('show_user_data')
    else:
        form = UserDataForm(instance=user_data)

    return render(request, 'edit_user_data.html', {'form': form, 'user_data': user_data})

def add_user_data(request):
    try:
        user_data = UserData.objects.get(user=request.user)
        editing = True
    except UserData.DoesNotExist:
        user_data = None
        editing = False

    if editing:
        # User data already exists, render edit form
        if request.method == 'POST':
            form = UserDataForm(request.POST, instance=user_data)
            if form.is_valid():
                form.save()
                return redirect('show_user_data')
        else:
            form = UserDataForm(instance=user_data)
        template_name = 'edit_user_data.html'
    else:
        # User data doesn't exist, render add form
        if request.method == 'POST':
            form = UserDataForm(request.POST)
            if form.is_valid():
                user_data = form.save(commit=False)
                user_data.user = request.user
                user_data.save()
                return redirect('show_user_data')
        else:
            form = UserDataForm()
        template_name = 'add_user_data.html'

    return render(request, template_name, {'form': form, 'user_data': user_data})
