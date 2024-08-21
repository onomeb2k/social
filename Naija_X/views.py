from django.shortcuts import render, redirect
from .models import Profile, Posts
from .forms import PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required



@login_required
def dashboard(request):
    if request.method == "POST":
        form = PostForm(request.POST or None)
        if form.is_valid():
            posts = form.save(commit=False)
            posts.user = request.user
            posts.save()
            return redirect("Naija_X:dashboard")
    
    followed_posts= Posts.objects.filter(
        user__profile__in=request.user.profile.follows.all()
    ).order_by("-created_at")    
    form = PostForm()
    return render(request, "Naija_X/dashboard.html",{'form':form, 'posts':followed_posts})

def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "Naija_X/profile_list.html", {"profiles": profiles})




def profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
	
    return render(request, "Naija_X/profile.html", {"profile": profile, })

    



#################### index####################################### 
def index(request):
	return render(request, 'Naija_X:dashboard')

########### register here ##################################### 
def register(request):
      
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			######################### mail system #################################### 
			htmly = get_template('Naija_X/email.html')
			d = { 'username': username }
			subject, from_email, to = 'welcome to Naija_X', 'your_email@gmail.com', email
			html_content = htmly.render(d)
			msg = EmailMultiAlternatives(subject, html_content, from_email, [to]) # type: ignore
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			################################################################## 
			messages.success(request, f'Your account has been created ! You are now able to log in')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'Naija_X/register.html', {'form': form,'title':'register here'})

################ login forms################################################### 
def Login(request):
	if request.method == 'POST':

		# AuthenticationForm_can_also_be_used__

		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username = username, password = password)
		if user is not None:
			form = login(request, user)
			messages.success(request, f' welcome {username} !!')
			return redirect('Naija_X:dashboard')
		else:
			messages.info(request, f'account does not exist, please sign in')
	form = AuthenticationForm()
	return render(request, 'registration/login.html', {'form':form, 'title':'log in'})

def Logout(request):
	logout(request)
	return redirect('Naija_X:login')
	


@login_required
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('Naija_X:profile') # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'Naija_X/profile.html', context)