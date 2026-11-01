from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegisterForm, TaskForm
from .models import Task


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        login(request, form.save())
        return redirect('task_list')
    return render(request, 'registration/register.html', {'form': form})


@login_required
def task_list(request):
    all_tasks = Task.objects.filter(user=request.user)
    tasks = all_tasks
    status, priority, q = request.GET.get('status', ''), request.GET.get('priority', ''), request.GET.get('q', '')
    if status:
        tasks = tasks.filter(status=status)
    if priority:
        tasks = tasks.filter(priority=priority)
    if q:
        tasks = tasks.filter(Q(title__icontains=q) | Q(description__icontains=q))
    stats = {
        'total': all_tasks.count(),
        'todo': all_tasks.filter(status='T').count(),
        'progress': all_tasks.filter(status='P').count(),
        'done': all_tasks.filter(status='D').count(),
    }
    return render(request, 'tasks/list.html', {
        'tasks': tasks, 'stats': stats, 'status': status, 'priority': priority, 'q': q,
        'status_choices': Task.STATUS, 'priority_choices': Task.PRIORITY,
    })


@login_required
def task_create(request):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        messages.success(request, 'Task created.')
        return redirect('task_list')
    return render(request, 'tasks/form.html', {'form': form, 'heading': 'New Task'})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        messages.success(request, 'Task updated.')
        return redirect('task_list')
    return render(request, 'tasks/form.html', {'form': form, 'heading': 'Edit Task'})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted.')
        return redirect('task_list')
    return render(request, 'tasks/confirm_delete.html', {'task': task})


@login_required
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.status = 'T' if task.status == 'D' else 'D'
        task.save(update_fields=['status'])
    return redirect(request.META.get('HTTP_REFERER') or 'task_list')
