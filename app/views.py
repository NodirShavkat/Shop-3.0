from django.shortcuts import render ,redirect
from .models import Category , Product, Comment
from django.http import JsonResponse
from app.forms import ProductModelForm,OrderModelForm, CommentModelForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q
from app.utils import filter_by_price
from django.db.models import Avg
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def index(request, category_id = None):
    search_query = request.GET.get('q','')
    filter_type = request.GET.get('filter_type','')
    
    categories = Category.objects.all()
    
    if category_id:
        products = Product.objects.filter(category = category_id)
    else:
        products = Product.objects.all()
        
    if search_query:
        products = products.filter(
            Q(name__icontains = search_query) | 
            Q(description__icontains=search_query)
        )

    products = filter_by_price(filter_type,products)
    
    products = products.annotate(
        avg_rating = Avg('comments__rating')
    )

    context = {
        'categories': categories,
        'products': products
    }
    return render(request,'app/home.html',context)



def detail(request, product_id):
    product = Product.objects.get(id = product_id)
    related_products = Product.objects.filter(category = product.category).exclude(id=product_id)
    comments = product.comments.filter(is_handle=False).order_by('-created_at')

    if not product:
        return JsonResponse(data={'message':'Oops. Page Not Found','status_code':404})
    
    avg_rating = comments.aggregate(Avg('rating'))['rating__avg'] or 0

    context = {
        'product': product,
        'comments': comments,
        'related_products': related_products,
        'avg_rating': avg_rating, 
    }
    return render(request,'app/detail.html',context)



# name = request.POST.get('name')



@login_required(login_url='/admin/')
def create_product(request):
    if request.method == 'POST':
        form = ProductModelForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Product successfully created ✅"
            )
            # add messages
            
            return redirect('app:create')
    else:
        form = ProductModelForm()
        
                
    context = {
        'form':form
    }
    return render(request,'app/create.html',context)


def delete_product(request,pk):
    product = Product.objects.get(id = pk)
    if product:
        product.delete()
        return redirect('app:index')    
    
    return render(request,'app/detail.html')



def update_product(request,pk):
    product = get_object_or_404(Product,pk=pk)
    if request.method == 'POST':
        form = ProductModelForm(request.POST,request.FILES,instance=product)

        if form.is_valid():
            form.save()
            return redirect('app:detail',pk)
    else:
        form = ProductModelForm(instance=product)
        
    context = {
        'form':form,
        'product':product
    }
    return render(request,'app/update.html',context)

def create_order(request,pk):
    product = get_object_or_404(Product,pk=pk)

    if request.method == 'POST':
        form = OrderModelForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            
            if order.quantity > product.stock:
                messages.add_message(request, messages.ERROR, 'Dont enough quantity', extra_tags='order') 
            else:
                product.stock -= order.quantity 
                product.save()
                order.save()
                messages.add_message(request, messages.SUCCESS, 'Order successfully sent✅', extra_tags='order') 
        else: 
            print(form.errors)
    else:
        form = OrderModelForm()

    context = {
        'form':form,
        'product':product
    }
    return render(request,'app/detail.html',context)

def create_comment(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = CommentModelForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment successfully sent', extra_tags='comment')
        else:
            print(form.errors)
    else:
        form = CommentModelForm()

    context = {
        'product': product,
        'comments': Comment.objects.filter(product=product).order_by('-created_at'),
    }
    return render(request, 'app/detail.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        full_message = f"From: {name} <{email}>\n\nMessage:\n{message}"

        send_mail(
            subject = f"Contact Me: {name}",
            message = full_message,
            from_email = settings.DEFAULT_FROM_EMAIL,
            recipient_list = ['muminovnodirjon3@gmail.com'],
            fail_silently = False,
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect('app:contact')
    return render(request, 'app/contact.html')