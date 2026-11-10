from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from app.forms import TaskForm
from app.models import Task

def home(request):
    tasks = Task.objects.order_by('id')
    return render(request, 'app/home.html', {
        'tasks': tasks,
        'pending_tasks': tasks.filter(is_completed=False),
        'completed_tasks': tasks.filter(is_completed=True),
        'pending_task_count': tasks.filter(is_completed=False).count(),
        'task_form': TaskForm(),
    })

@require_POST
def add_task(request):
    form = TaskForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'app/home.html', {
        'tasks': Task.objects.order_by('id'),
        'pending_tasks': Task.objects.filter(is_completed=False).order_by('id'),
        'completed_tasks': Task.objects.filter(is_completed=True).order_by('id'),
        'pending_task_count': Task.objects.filter(is_completed=False).count(),
        'task_form': form,
    }, status=400)

def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'app/edit.html', {
        'task': task,
        'form': form,
    })

@require_POST
def mark_done(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.is_completed = True
    task.save(update_fields=['is_completed'])
    return redirect('home')

@require_POST
def mark_undone(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.is_completed = False
    task.save(update_fields=['is_completed'])
    return redirect('home')

@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return redirect('home')