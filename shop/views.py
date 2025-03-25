from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.utils import timezone
from .models import Category, Product, Wishlist, Cart, CartItem, MonthlyProfit
from .forms import UserRegistrationForm
from django.http import JsonResponse
import json
from decimal import Decimal

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    query = request.GET.get('q')
    cart = None
    cart_product_ids = []

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_product_ids = list(cart.items.values_list('product_id', flat=True))

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'query': query,
        'cart': cart,
        'cart_product_ids': cart_product_ids
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    
    # Проверяем, есть ли товар в корзине
    in_cart = False
    cart_quantity = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            in_cart = True
            cart_quantity = cart_item.quantity
    
    context = {
        'product': product,
        'in_cart': in_cart,
        'cart_quantity': cart_quantity
    }
    return render(request, 'shop/product/detail.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Создаем избранное для нового пользователя
            Wishlist.objects.create(user=user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('shop:product_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'shop/register.html', {'form': form})

@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_product_ids = list(cart.items.values_list('product_id', flat=True))
    
    context = {
        'wishlist': wishlist,
        'cart': cart,
        'cart_product_ids': cart_product_ids
    }
    return render(request, 'shop/wishlist.html', context)

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        status = 'removed'
    else:
        wishlist.products.add(product)
        status = 'added'
    
    if request.headers.get('Content-Type') == 'application/json':
        return JsonResponse({'status': status})
    
    return redirect(request.META.get('HTTP_REFERER', 'shop:product_list'))

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist.products.remove(product)
    messages.success(request, f'Товар "{product.name}" удален из избранного')
    return redirect(request.META.get('HTTP_REFERER', 'shop:product_list'))

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart = Cart.objects.filter(user=request.user).first()
        
        if not cart:
            cart = Cart.objects.create(user=request.user)
        
        cart_item = cart.items.filter(product=product).first()
        
        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart.items.create(product=product, quantity=1)
        
        # Для AJAX запросов
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({
                'status': 'success',
                'cart_total': str(cart.total_price),
                'message': 'Товар добавлен в корзину'
            })
        
        # Для обычных POST запросов
        messages.success(request, 'Товар добавлен в корзину')
        return redirect(request.META.get('HTTP_REFERER', 'shop:product_list'))
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        messages.success(request, 'Товар удален из корзины')
    return redirect('shop:cart')

@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
            
    return redirect('shop:cart')

@login_required
def clear_cart(request):
    if request.method == 'POST':
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()
        messages.success(request, 'Корзина очищена')
    return redirect('shop:cart')

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'shop/cart.html', {'cart': cart})

@login_required
def checkout(request):
    if request.method == 'POST':
        cart = get_object_or_404(Cart, user=request.user)
        
        if not cart.items.exists():
            messages.warning(request, 'Ваша корзина пуста')
            return render(request, 'shop/cart.html', {'cart': cart})
        
        # Получаем текущий месяц
        current_month = timezone.now().replace(day=1)
        
        # Получаем или создаем запись о прибыли за текущий месяц
        monthly_profit, created = MonthlyProfit.objects.get_or_create(
            month=current_month,
            defaults={'profit': Decimal('0.00')}
        )
        
        # Добавляем сумму корзины к прибыли
        monthly_profit.profit += cart.total_price
        monthly_profit.save()
        
        # Уменьшаем количество товаров на складе
        for item in cart.items.all():
            product = item.product
            product.stock -= item.quantity
            product.save()
        
        # Очищаем корзину
        cart.items.all().delete()
        
        messages.success(request, 'Спасибо за покупку!')
        return render(request, 'shop/cart.html', {'cart': cart})
    
    return render(request, 'shop/cart.html', {'cart': cart})
