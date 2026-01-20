from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from testapp.forms import Signup
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm
from django.core.paginator import Paginator

@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)

    # Filters
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    search = request.GET.get('search')

    if status:
        tasks = tasks.filter(status=status)
    if priority:
        tasks = tasks.filter(priority=priority)
    if search:
        tasks = tasks.filter(title__icontains=search)

    pending_tasks = tasks.filter(status='Pending')
    completed_tasks = tasks.filter(status='Completed')

    return render(request, 'testapp/dashboard.html', {
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks
    })

@login_required
def task_create(request):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        messages.success(request, "Task added successfully.")
        return redirect('dashboard')

    return render(request, 'testapp/task_form.html', {'form': form})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    form = TaskForm(request.POST or None, instance=task)

    if form.is_valid():
        form.save()
        messages.success(request, "Task updated successfully.")
        return redirect('dashboard')

    return render(request, 'testapp/task_form.html', {'form': form})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, "Task deleted successfully.")
        return redirect('dashboard')

    return render(request, 'testapp/task_confirm_delete.html', {'task': task})


@login_required
def mark_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.status = 'Completed'
    task.save()
    messages.success(request, "Task marked as completed.")
    return redirect('dashboard')

@login_required
# Home page
def main(request):
    return render(request, 'testapp/main.html')


# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = Signup()

    return render(request, 'testapp/signup.html', {'form': form})

def main(request):
    return render(request,'testapp/main.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'testapp/login.html', {'form': form})
# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')
