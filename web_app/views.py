from django.shortcuts import redirect, render, HttpResponse
from web_app.models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q




@never_cache
def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('base')
        else:
            return redirect('main')
    else: 
        return render(request, 'home.html')


#user login page
@never_cache
def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser :
            return redirect('base')
        else:
            return redirect('main')
    else:
       return redirect('main')
    

#signup page
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        username = username.strip()
        first_name = request.POST['first_name']
        first_name = first_name.strip()
        last_name = request.POST['last_name']
        last_name = last_name.strip()
        email = request.POST['email']
        email = email.strip()
        password = request.POST['password']
        conformpassword = request.POST['c-password']
        if first_name=='':
            return redirect('signup')
        elif last_name=='':
            return redirect('signup')
        elif username=='':
            return redirect('signup')
        elif User.objects.filter(username=username).exists():
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            return redirect('signup')
        elif email=='':
            return redirect('signup')
        elif password=='':
            return redirect('signup')
        elif len(password)<6:
            return redirect('signup')
        elif password != conformpassword:
            return redirect('signup')
        
        else:
            myuser = User.objects.create_user(
                username = username,
                first_name = first_name,
                last_name = last_name, 
                email=email, 
                password = password, 
            )
        
            myuser.save()
            return redirect('login')

    return render(request, 'signup.html')


#search function
@never_cache
def admin_page(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            CS_user = User.objects.all()
            
            search=request.GET.get('query','')

            if search:
                CS_user= CS_user.filter(
                    Q(username__icontains = search) |
                    Q(email__icontains = search)
                )

            context = {
                'CS_user' : CS_user,
            }
            return render(request, 'admin_page.html',context)
        else:
            return redirect('user_page')
    else:
        return redirect('home')
def search(request):
    query = request.GET['query']
    allCustomUser = CustomUser.objects.filter(name__icontains=query)
    context = {
        'allCustomUser':CustomUser
    }
    return render(request, 'search.html', context)



# add user
@never_cache
def Add(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            first_name = first_name.strip()
            last_name = request.POST.get('last_name')
            last_name = last_name.strip()
            username = request.POST.get('username')
            username = username.strip()
            email = request.POST.get('email')
            email = email.strip()
            
            if first_name=='':
                messages.error(request, 'First name should not be null')
                return redirect('base')
            elif last_name=='':
                messages.error(request, 'Last name should not be null')
                return redirect('base')
            elif username=='':
                messages.error(request, 'Username should not be null')
                return redirect('base')
            elif User.objects.filter(username=username).exists():
                messages.error(request,'!!!User is already exists!!!')
                return redirect('base')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'E-mail id is already exists')
                return redirect('base')
            elif email=='':
                messages.error(request, 'E-mail should not be null')
                return redirect('base')
        
            User.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
            )
            return redirect('base') 
        
    else:
        return redirect('admin_log')



# Edit user
@never_cache
def Edit(request):
    if request.user.is_superuser:
        CS_user = User.objects.all()

        context = {
            'CS_user' : CS_user
        }

        return redirect(request, 'admin_page.html', context)
    else:
        return redirect('admin_log')



# update user
@never_cache
def Update(request, id):
    if request.user.is_superuser:    
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            first_name = first_name.strip()
            last_name = request.POST.get('last_name')
            last_name = last_name.strip()
            username = request.POST.get('username')
            username = username.strip()
            email = request.POST.get('email')
            email = email.strip()

            if first_name=='':
                messages.error(request, 'First name should not be null')
                return redirect('base')
            elif last_name=='':
                messages.error(request, 'Last name should not be null')
                return redirect('base')
            elif username=='':
                messages.error(request, 'Username should not be null')
                return redirect('base')
            elif User.objects.filter(username=username).exists():
                messages.error(request,'Username is already exists')
                return redirect('base')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'E-mail id is already exists')
                return redirect('base')
            elif email=='':
                messages.error(request, 'E-mail should not be null')
                return redirect('base')
            
        User.objects.create_user(
            id = id,
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email,
        )
        
        return redirect('base')

    
    else:
        return redirect('admin_log')


# delete user
@never_cache
def delete(request, id):
    if request.user.is_superuser:
        CS_user = User.objects.filter(id = id)
        CS_user.delete()

        context = {
            'CS_user' : CS_user
        }
        return redirect('base')
    else:
        return redirect('admin_log')


#login admin
@never_cache
def admin_log(request):
    if request.user.is_authenticated:
        if  request.user.is_superuser:
            
            return redirect('base')
        else:
            return redirect('user_page')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            username = username, 
            password = password
            )
        
        if user and user.is_superuser:
            login(request , user)
            return redirect('base') 
          
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('admin_log')
    else:
        if request.user.is_superuser:
            return redirect('base')
    return render(request , "admin_log.html")


@never_cache
def logoutt(request):
    logout(request)
    return redirect('home')
    


#user logout
@never_cache
def user_page(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('main')
        else:
            return render(request, 'logout.html')
    else:
        return redirect('home')
    


@never_cache
def main(request):
    if request.user.is_authenticated:
        if  request.user.is_superuser:
            
            return redirect('base')
        else:
            return redirect('user_page')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            
            username = username, 
            password = password
            )
        if user is not None and not user.is_superuser:
            login(request, user)
            return redirect('user_page') 
        elif user:
            messages.error(request,'login with admin')
        else:
            messages.error(request, 'Invalid username or password')          
    return render(request,'login.html')
    