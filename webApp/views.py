from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import (get_object_or_404,
                              render,
                              redirect,
                              HttpResponseRedirect)
from django.contrib.auth.decorators import login_required
 
# relative import of forms
from .models import TransactionModel
from .forms import TransactionForm


def home_view(request):
    context = {}
    if request.user.is_authenticated:
        # User is logged in
        #logged_in_username = request.user.username
        user = request.user.get_username()
        print(f"home_view logged-in user={user}")
        context["dataset"] = TransactionModel.objects.filter(owner__username=user)
        return render(request, 'index.html', context)
    else:
        # No user logged in
        print(f"home_view no logged-in user")
        return redirect('login')


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    #context = {}
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Create form with POST data
        if form.is_valid():
            # Extract username and password from the validated form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f"login_view user {username} is trying to log in")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to successful login page (optional)
                return redirect('home')
            else:
                # Login failed (invalid credentials)
                error_message = "Invalid username or password."
        else:
            # Form is invalid (e.g., missing fields)
            error_message = "Please fill out both username and password fields."
    else:
        form = AuthenticationForm()  # Create an empty form for GET requests
        error_message = None  # No previous errors

    return render(request, 'login.html', {'error_message': error_message, 'form':form})
    #return render(request, 'login.html', context)


@login_required
def create_view(request):
    # dictionary for initial data with 
    # field names as keys
    context = {}
 
    # add the dictionary during initialization
    form = TransactionForm(request.POST or None)
    if form.is_valid():
        form.save()
         
    context['form'] = form
    return render(request, "create_view.html", context)


@login_required
def list_view(request):
    user = request.user.get_username()
    print(f"list_view user={user}")
    
    # dictionary for initial data with field names as keys
    context = {}
 
    # add the dictionary during initialization
    #context["dataset"] = TransactionModel.objects.all() #.order_by("-id")
    context["dataset"] = TransactionModel.objects.filter(owner__username=user)
         
    return render(request, "list_view.html", context)


def detail_view(request, id):
    # dictionary for initial data with 
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    context["data"] = TransactionModel.objects.get(id = id)
         
    return render(request, "detail_view.html", context)


def update_view(request, id):
    # dictionary for initial data with field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(TransactionModel, id = id)
 
    # pass the object as instance in form
    form = TransactionForm(request.POST or None, instance = obj)
 
    # save the data from the form and redirect to detail_view
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/") #+id)
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "update_view.html", context)


# delete view for details
def delete_view(request, id):
    # dictionary for initial data with field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(TransactionModel, id = id)
 
 
    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to home page
        return HttpResponseRedirect("/")
 
    return render(request, "delete_view.html", context)