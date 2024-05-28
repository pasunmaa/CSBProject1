from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import (get_object_or_404,
                              render,
                              redirect,
                              HttpResponseRedirect)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
 
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
                query = f"SELECT * FROM webApp_transactionmodel WHERE owner_id = '{userid}' AND note LIKE '{note_start}%'"
                print(f"query={Fore.BLUE}{query}{Style.RESET_ALL}")
                dataset = TransactionModel.objects.raw(query)
                # SECURE QUERY
                # dataset = TransactionModel.objects.filter(owner__username=user, note__startswith=note_start)
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


def lockout(request, credentials, *args, **kwargs):
    error_message = "Locked out due to too many login failures. Contact admin."
    form = AuthenticationForm()  # Create an empty form for GET requests
    return render(request, 'login.html', {'error_message': error_message, 'form':form})


def login_view(request):
    #context = {}
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Create form with POST data
        if form.is_valid():
            # Extract username and password from the validated form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f"login_view user {username} is trying to log in")
            try:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    try:
                        login(request, user)
                        # Redirect to successful login page (optional)
                        return redirect('home')
                    except Exception as e:
                        error_message = f"Login failed. {e}"
                else:
                    # Login failed (invalid credentials)
                    error_message = "Invalid username or password."
            except Exception as e:  # Catch broader exception (consider specific exceptions later)
                if getattr(request, 'status_code', None) == 429:
                    error_message = "Too many login attempts. Please try again later."
                else:
                    error_message = f"Authentication failed. {e}"
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


# Authentication works properly when @login_required is set on top of the function
#@login_required
def detail_view(request, id):
    # dictionary for initial data with field names as keys
    context ={}
 
    try:
        obj = TransactionModel.objects.get(id = id)
        #print(f"udpate view: user='{request.user}', obj owner='{obj.owner}'")
        # INSECURE authorisation missing
        context["data"] = obj
        # SECURE authorisation checked
        '''
        if str(request.user) == str(obj.owner):
            context["data"] = obj
        else:
            context['error_message'] = "Permission denied"    
        '''
    except TransactionModel.DoesNotExist:
        # return empty data
        error_message = "Record not found."
        context['error_message'] = error_message
        pass
 
    return render(request, "detail_view.html", context)


@login_required
def update_view(request, id):
    # dictionary for initial data with field names as keys
    context ={}
    #print(f"udpate view: request user='{request.user}'")
 
    # fetch the object related to passed id
    obj = get_object_or_404(TransactionModel, id = id)
 
    # pass the object as instance in form
    form = TransactionForm(request.POST or None, instance = obj)
 
    # save the data from the form and redirect to detail_view
    if form.is_valid():
        user = request.user.get_username()
        #print(f"udpate view: user='{user}', obj owner='{obj.owner}'")
        #print(f"udpate view: user='{type(user)}', obj owner='{type(obj.owner)}'")
        if str(user) == str(obj.owner):
            form.save()
            return HttpResponseRedirect("/") #+id)
        else:
            # 403 = PermissionDenied
            return HttpResponse("Permission Denied", status=403)
 
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
        user = request.user.get_username()
        if str(user) == str(obj.owner):
            obj.delete()
            # after deleting redirect to home page
            return HttpResponseRedirect("/")
        else:
            return HttpResponse("Permission Denied", status=403)
 
    return render(request, "delete_view.html", context)