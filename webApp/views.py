from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import (get_object_or_404,
                              render,
                              redirect,
                              HttpResponseRedirect)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
 
# relative import of forms
from .models import TransactionModel
from .forms import TransactionForm, TransactionFilterForm

# color library for console printing
from colorama import Fore, Style


def home_view(request):
    
    if request.user.is_authenticated:
        context = {}
        dataset = TransactionModel.objects.none()  # Initial empty queryset

        # User is logged in
        user = request.user.get_username()
        #print(f"home_view logged-in user={user}")
        
        userid = User.objects.get(username=user).id
        print(f"home_view logged-in user={user}, user id={userid}")
        
        # Handle form submission and filtering
        form = TransactionFilterForm(request.GET)
        
        if form.is_valid():
            note_start = form.cleaned_data['note_startswith']
            print(f"home_view note_startswith={note_start}")
            if note_start and (note_start != ''):
                # Filter by note
                # INSECURE QUERY
                query = f"SELECT * FROM webApp_transactionmodel WHERE owner_id = '{userid}' AND note LIKE '{note_start}'"
                print(f"query={Fore.BLUE}{query}{Style.RESET_ALL}")
                dataset = TransactionModel.objects.raw(query)
                # SECURE QUERY
                dataset = TransactionModel.objects.filter(owner__username=user, note__startswith=note_start)
            else:
                dataset = TransactionModel.objects.filter(owner__username=user)
        else:
            dataset = TransactionModel.objects.filter(owner__username=user)

        context = {
            'dataset': dataset,
            'form': form,  # Pass the form to the template
        }
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
def list_view(request):
    user = request.user.get_username()
    print(f"list_view user={user}")
    print(f"list_view request={request}")
    
    # dictionary for initial data with field names as keys
    context = {}
 
    # add the dictionary during initialization
    #context["dataset"] = TransactionModel.objects.all() #.order_by("-id")
    context["dataset"] = TransactionModel.objects.filter(owner__username=user)

    #query = 'SELECT * FROM webApp_transactionmodel WHERE last_name = %s' **% lname**
         
    return render(request, "list_view.html", context)


@login_required
def create_view(request):
    # dictionary for initial data with field names as keys
    context = {}
 
    # add the dictionary during initialization
    form = TransactionForm(request.POST or None)
    if form.is_valid():
        form.instance.owner = request.user  # Set owner on the form instance
        form.save()
         
    context['form'] = form
    return render(request, "create_view.html", context)


# Authorization works properly when @login_required is set on top of the function
#@login_required
def detail_view(request, id):
    # dictionary for initial data with field names as keys
    context ={}
 
    # add the dictionary during initialization
    try:
        context["data"] = TransactionModel.objects.get(id = id)
    except TransactionModel.DoesNotExist:
        # return empty data
        pass

    return render(request, "detail_view.html", context)


@login_required
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
 
    # add form to context
    context["form"] = form
 
    return render(request, "update_view.html", context)


@login_required
def delete_view(request, id):
    # dictionary for initial data with field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(TransactionModel, id = id)
 
 
    if request.method =="POST":
        obj.delete()
        # after deleting redirect to home page
        return HttpResponseRedirect("/")
 
    return render(request, "delete_view.html", context)