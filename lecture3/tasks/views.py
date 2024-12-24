from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

class NewForm(forms.Form):
    task = forms.CharField(label="New Task")

class RemoveForm(forms.Form):
    task = forms.CharField(label="Remove Task")

# View for listing tasks
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []

    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })

# View for adding tasks
def add(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            print(request.session["tasks"])  # Debug output
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })
    return render(request, "tasks/add.html", {
        "form": NewForm()
    })

# View for removing tasks
def remove(request):
    if request.method == "POST":
        form = RemoveForm(request.POST)
        if form.is_valid():
            task = request.POST.get("task")  # Get the task to remove from the POST data
            tasks = request.session.get("tasks", [])  # Get the current tasks from the session
            if task in tasks:
                tasks.remove(task)  # Remove the task from the list
                request.session["tasks"] = tasks  # Debug output
                return HttpResponseRedirect(reverse("tasks:index"), {
                     "success": f"Task '{task}' has beeen removed"
                })
            else:
                # If the task does not exist, return an error message
                return render(request, "tasks/remove.html", {
                    "form": form,
                    "error": f"Task '{task}' not found in the list."
                })
        else:
            return render(request, "tasks/remove.html", {
                "form": form
            })
    return render(request, "tasks/remove.html", {
        "form": RemoveForm()
    })