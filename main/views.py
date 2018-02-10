from django.http import HttpResponse, JsonResponse, Http404
from main.models import *
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from main.forms import *
from django.contrib.auth import authenticate, login, logout
from main.forms import UserSignupForm, UserLoginForm
from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Message
from django.db.models import Q
from django.conf import settings
 
def messages(request):
	 recipient_id = request.POST.get("recipient")
	 recipient_object = CustomUser.settings.AUTH_USER_MODEL(id=recipient_id)
	 Message.objects.create(
		 text=request.POST.get("message"),
		recipient=recipient_object,
		 user=request.user
	)
	 return redirect("chat")

def detail(request):
	if request.method == "POST":
		Message.objects.create(text=request.POST.get("message"), recipient=request.POST.get("recipient"), user=request.user)
	
	context={
	'messages': Message.objects.all()
	}
	return render(request,'detail.html', context)
def save_message(request, message_id):
	message = Message.objects.get(id=message_id)
	message.save()
	
	return redirect("/chat/")

def chat_list(request):
	# sender = User.objects.get(id=sender_id)
	# request.user.recipient.all()
	msgs= Message.objects.filter(recipient=request.user)
	users = []
	for msg in msgs:
		users.append(msg.user)
	users = list(set(users))
	context={
	'chat_list': users,
	}
	return render(request,'chat_list.html',context)
def chat(request, sender_id):
	msgs_received = Message.objects.filter(recipient=request.user)
	msgs_received = msgs_received.filter(user__id=sender_id)
	msgs_sent = Message.objects.filter(user=request.user)
	msgs_sent = msgs_sent.filter(recipient__id=sender_id)
	msgs = msgs_received | msgs_sent
	msgs = msgs.distinct().order_by("time")
	
	context = {
		'messages': msgs_received,
		'msgs_sent': msgs_sent,
		'recipient': sender_id,
		'msgs': msgs
	}
	return render(request,'chat.html', context)

@staff_member_required


def likes(request, myfeed_id):
	myfeed = Myfeed.objects.get(id=myfeed_id)

	impressed, created = Like.objects.get_or_create(user=request.user, myfeed=myfeed)
	if created:
		action="like"
	else:
		action="unlike"
		impressed.delete()

	myfeed_like_count = Like.objects.filter(myfeed=myfeed).count()

	context = {
		"action":action,
		"count":myfeed_like_count
	}
	return JsonResponse(context, safe=False)

def wish_list(request):
	myfeed = request.user
	mywishlist = myfeed.like_set.all()
	context = {
	
	"liked":mywishlist,
	}
	return render(request, 'wish_list.html', context)


def myfeed_list(request):
	object_list = Myfeed.objects.all().order_by('-timestamp')
	query = request.GET.get('search')
	if query:
		object_list = object_list.filter(
			Q(username__icontains=query)|
			Q(book__icontains=query)|
			Q(feed__icontains=query)|
			Q(major__icontains=query)|
			Q(course__icontains=query)
			).distinct()
	context = {
	"object_list": object_list,
	}
	return render(request, 'myfeed_list.html', context)


def myfeed_detail(request, pk):
	instance = Myfeed.objects.get(pk=pk)
	form = MyfeedForm()

	liked = False
	if request.user.is_authenticated:
		if Like.objects.filter(myfeed=instance, user=request.user).exists():
			liked = True
	myfeed_like_count = Like.objects.filter(myfeed=instance).count()

	if request.method=="POST":
		form = ReplyForm(request.POST)
		if form.is_valid():
			reply = form.save(commit=False)
			reply.myfeed=instance
			reply.user=request.user
			reply.save()
			return redirect("detail", pk=instance.id)

	replys = Reply.objects.filter(myfeed=instance).order_by("timestamp")

	context = {
	"replys":replys,
	"form":form,
	"instance": instance,
	"liked":liked,
	"count":myfeed_like_count
	}
	return render(request, 'myfeed_detail.html', context)



def Myfeed_create(request):
	if not request.user.is_authenticated:
		return redirect('login')
	form = MyfeedForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		myfeed = form.save(commit=False)
		myfeed.author=request.user
		myfeed.save()
		return redirect("list")
	context = {
	"form": form,
	}
	return render(request, 'myfeed_create.html', context)

def myfeed_update(request, pk):
	instance = Myfeed.objects.get(pk=pk)
	form = MyddeForm(request.POST or None, request.FILES or None, instance = instance)
	if form.is_valid():
		form.save()
		return redirect('list')
	context = {
	"form":form,
	"instance": instance,
	}
	return render(request, 'myfeed_update.html', context)


@staff_member_required

def myfeed_create(request):
	if not request.user.is_authenticated:
		return redirect('list')
	form = MyfeedForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		myfeed = form.save(commit=False)
		myfeed.user=request.user
		myfeed.save()
		return redirect("list")
	context = {
	"form": form,
	}
	return render(request, 'myfeed_create.html', context)

@staff_member_required
def myfeed_update(request, pk):
	instance = Myfeed.objects.get(pk=pk)
	form = MyfeedForm(request.POST or None, request.FILES or None, instance = instance)
	if form.is_valid():
		form.save()
		return redirect('list')
	context = {
	"form":form,
	"instance": instance,
	}
	return render(request, 'myfeed_update.html', context)

@staff_member_required
def myfeed_delete(request, pk):
	Myfeed.objects.get(pk=pk).delete()
	return redirect('list')

def sign_up(request):
	form = UserSignupForm()
	if request.method=="POST":
		print ("post request")
		form = UserSignupForm(request.POST)
		if form.is_valid():
			print ("form valid")
			person = form.save(commit=False)
			person.set_password(person.password)
			person.save()

			login(request, person)
			return redirect('list')

	print(form.errors)
	context = {
		"signup_form":form,
	}
	return render(request, 'signup.html', context)



def login_view(request):
	context = {}
	context['form'] = UserLoginForm()
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			auth_user = authenticate(username=email, password=password)
			if auth_user is not None:
				login(request, auth_user)
				return redirect('list')
	return render(request, 'login.html', context)


def logout_view(request):
	logout(request)
	return redirect('/signup/')

def profile_page(request):
	context = {}
	print (request.user)
	print (request.user.pk)
	try:
		context['user'] = CustomUser.objects.get(pk=request.user.pk)
	except Exception as e:
		raise Http404('404')
	return render(request, 'profile_page.html', context)

def edit_profile(request):
	context = {}
	try:
		user = CustomUser.objects.get(pk=request.user.pk)
	except Exception as e:
		raise Http404('404')
	form = EditProfileForm(request.POST or None, instance=user)
	context['form'] = form
	if form.is_valid():
		form.save()
		return redirect('/profile/')
	else:
		print (form.errors)
	return render(request, 'edit_profile.html', context)
