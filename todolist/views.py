from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from todolist.forms import TodoForm, TodoListForm
from todolist.models import Todo, TodoList

def index(request):
    return render(request, "todolist/index.html", {"form": TodoForm()})

def todolist(request, todolist_id):
    todolist = get_object_or_404(TodoList, pk=todolist_id)
    if request.method == "POST":
        redirect('todolist:add_todo', todolist_id=todolist_id)
    
    return render(
        request,
        "todolist/todolist.html",
        {"todolist": todolist, "form": TodoForm()}
    )
    
def add_todo(request, todolist_id):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            user = request.user if request.user.is_authenticated else None
            todo = Todo(
                description=request.POST["description"],
                todolist_id = todolist_id,
                creator=user,
            )
            todo.save()
            return redirect("todolist:todolist", todolist_id=todolist_id)
        else:
            return render(request, "todolist/todolist.html", {"form": form})
    return redirect("todolist:index")

@login_required
def overview(request):
    if request.method == "POST":
        return redirect("todolist:add_todolist")
    return render(request, "todolist/overview.html", {"form": TodoListForm()})

def new_todolist(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            user = request.user if request.user.is_authenticated else None
            todolist = TodoList(creator=user)
            todolist.save()
            todo = Todo(
                description=request.POST["description"],
                todolist_id = todolist.id,
                creator = user,
            )
            todo.save()
            return redirect("todolist:todolist", todolist_id=todolist.id)
        
        else:
            return render(request, "todolist/index.html", {"form": form})
        
    return redirect("todolist:index")

def add_todolist(request):
    if request.method == "POST":
        form = TodoListForm(request.POST)
        if form.is_valid():
            user = request.user if request.user.is_authenticated else None
            todolist = TodoList(title=request.POST['title'], creator=user)
            todolist.save()
            return redirect("todolist:todolist", todolist_id=todolist.id)
        else:
            return render(request, "todolist/overview.html", {"form": form})
        
    return redirect("todolist:index")
 
