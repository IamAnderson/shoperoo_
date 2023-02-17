from django.shortcuts import render, get_object_or_404, redirect
from .models import Category,Item, Messages,History, Cart
from .forms import SignupForm, NewItemForm, EditItemForm,Convo
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from itertools import chain


# Create your views here.
@login_required
def index(request):
	item = Item.objects.filter(is_sold=False)[0:6]
	category = Category.objects.all()
	
	recommends = History.objects.filter(user=request.user)
	rec_item=[]
	for recommend in recommends:
		items=Item.objects.filter(is_sold=False, category=recommend.item.category).exclude(created_by=request.user)
		print(recommend.item.created_by)
		rec_item.append(items)

	rec_list = list(chain(*rec_item))[0:6]
	
	return render(request, 'index.html', {"category":category, "item": item, "rec_item": rec_list})



def detail(request, pk):
	item =get_object_or_404(Item, pk=pk)
	related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
	return render(request, 'detail.html', {'item':item, 'related_items': related_items})


def contact(request):
	return render(request, 'contact.html')

def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/login/')
	else:
		form = SignupForm()
	return render(request, 'signup.html', {'form':form})

@login_required
def newitem(request):
	if request.method == 'POST':
		
		form = NewItemForm(request.POST, request.FILES)
		
		if form.is_valid():
			
			item = form.save(commit=False)
			item.created_by = request.user
			item.save()

			return redirect('detail', pk=item.id)
	else:
		form = NewItemForm()
	return render (request, 'newitem.html', {'form':form, 'title': "New item"})


@login_required
def dashboard(request):
	items = Item.objects.filter(created_by=request.user)
	return render(request, "dashboard.html", {'items':items, 'title': "Dashboard"})


@login_required
def delete(request,pk):
	item = get_object_or_404(Item, pk=pk, created_by=request.user)
	item.delete()
	return redirect('dashboard')
@login_required
def edititem(request,pk):
	item = get_object_or_404(Item, pk=pk, created_by=request.user)
	
	if request.method == 'POST':
		form = EditItemForm(request.POST,request.FILES, instance=item)
		
		if form.is_valid():
			form.save()

			return redirect('detail', pk=item.id)
	else:
		form = EditItemForm(instance=item)
	return render (request, 'newitem.html', {'form':form, 'title': "Edit item"})

def browse(request):
	query = request.GET.get('query', '')
	category_id = request.GET.get('category',0)
	categories = Category.objects.all()
	items = Item.objects.filter(is_sold=False)
	if category_id:
		items = items.filter(category_id = category_id)
	if query:
		items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

	return render (request, 'browse.html', {'items':items, 'query':query, 'categories': categories, 'category_id': int(category_id)})


@login_required
def new_message(request, item_pk):
	item = get_object_or_404(Item, pk=item_pk)

	if item.created_by == request.user:
		return redirect('dashboard')

	messages = Messages.objects.filter(item=item).filter(members__in=[request.user.id])

	if messages:
		return redirect('message', pk=messages.first().id)

	if request.method =='POST':
		form = Convo(request.POST)

		if form.is_valid():
			messages = Messages.objects.create(item=item)
			messages.members.add(request.user)
			messages.members.add(item.created_by)
			messages.save()

			convo_message = form.save(commit=False)
			convo_message.conversation = messages
			convo_message.created_by = request.user
			convo_message.save()
			
			return redirect('detail', pk=item_pk)

	else:
		form = Convo()

	return render(request, 'new_message.html', {
		'form': form
	})
	
@login_required
def inbox(request):
	
	messages = Messages.objects.filter(members__in=[request.user.id])
	return render(request, 'inbox.html', {'messages':messages})

	
@login_required
def message(request,pk):
	
	messages = Messages.objects.filter(members__in=[request.user.id]).get(pk=pk)
	if request.method == "POST":
		form = Convo(request.POST)
		if form.is_valid():
			convo_message=form.save(commit=False)
			convo_message.conversation = messages
			convo_message.created_by = request.user
			convo_message.save()
			messages.save()

			return redirect('message', pk=pk)
	else:
		form = Convo()


	return render(request, 'message.html', {'messages':messages , 'form': form})

@login_required
def addtocart(request, pk):
	item = get_object_or_404(Item, pk=pk)
	if Cart.objects.filter(item=item).exists():
		message = 'already in cart'
	else:
		new_item= Cart.objects.create(user=request.user, item=item)
		add_history= History.create(user=request.user, item=item)
		new_item.save()
		add_history.save()

	related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
	return render(request, 'detail.html', {'item':item, 'related_items': related_items, 'message':message})

@login_required
def cart(request):
	items= Cart.objects.filter(user=request.user)
	return render(request, 'cart.html', {'items':items})

@login_required
def remove(request,pk):
	item = get_object_or_404(Cart, pk=pk, user=request.user)
	item.delete()
	return redirect('cart')


