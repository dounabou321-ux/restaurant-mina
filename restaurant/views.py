from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import Category, Dish, Order
import json


def staff_required(view_func):
    """Decorator to require staff status"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')
        if not request.user.is_staff:
            messages.error(request, "Accès réservé aux administrateurs.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def home(request):
    """Home page view"""
    categories = Category.objects.filter(is_active=True).prefetch_related('dishes')
    return render(request, 'core/home.html', {'categories': categories})


def menu(request):
    """Menu page view with category filtering"""
    categories = Category.objects.filter(is_active=True).prefetch_related('dishes')
    selected_category = request.GET.get('category')
    search_query = request.GET.get('q')
    
    dishes = Dish.objects.filter(is_available=True)
    
    if selected_category:
        dishes = dishes.filter(category_id=selected_category)
    
    if search_query:
        dishes = dishes.filter(name__icontains=search_query)
    
    return render(request, 'core/menu.html', {
        'categories': categories,
        'dishes': dishes,
        'selected_category': selected_category
    })


def cart(request):
    """Cart view"""
    return render(request, 'core/cart.html')


def checkout(request):
    """Checkout view"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            table_number = data.get('table_number')
            items = data.get('items', [])
            special_instructions = data.get('special_instructions', '')
            
            if not table_number or not items:
                return JsonResponse({'success': False, 'error': 'Données invalides'})
            
            # Calculate total
            total = 0
            order_items = []
            for item in items:
                dish = Dish.objects.get(id=item['id'])
                quantity = int(item['quantity'])
                item_total = float(dish.price) * quantity
                total += item_total
                order_items.append({
                    'id': dish.id,
                    'name': dish.name,
                    'price': float(dish.price),
                    'quantity': quantity,
                    'total': item_total
                })
            
            # Create order
            order = Order.objects.create(
                table_number=table_number,
                items=order_items,
                total_amount=total,
                special_instructions=special_instructions,
                status='pending'
            )
            
            return JsonResponse({
                'success': True,
                'order_id': order.order_id,
                'total': total
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return render(request, 'core/checkout.html')


def order_confirmed(request, order_id):
    """Order confirmation view"""
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'core/order_confirmed.html', {'order': order})


@staff_required
def dashboard(request):
    """Staff dashboard view"""
    orders = Order.objects.all()[:50]
    categories = Category.objects.all()
    dishes = Dish.objects.all()
    return render(request, 'dashboard/orders.html', {
        'orders': orders,
        'categories': categories,
        'dishes': dishes
    })


@staff_required
def menu_management(request):
    """Menu management view for staff"""
    categories = Category.objects.all().prefetch_related('dishes')
    return render(request, 'dashboard/menu_management.html', {'categories': categories})


@staff_required
def kitchen_view(request):
    """Kitchen view for preparing orders"""
    pending_orders = Order.objects.filter(status__in=['pending', 'preparing']).order_by('created_at')
    return render(request, 'dashboard/kitchen_view.html', {'orders': pending_orders})


@staff_required
@require_http_methods(["POST"])
def update_order_status(request):
    """Update order status API"""
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        new_status = data.get('status')
        
        order = Order.objects.get(order_id=order_id)
        order.status = new_status
        order.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@staff_required
def add_dish(request):
    """Add new dish"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        is_available = request.POST.get('is_available') == 'on'
        
        Dish.objects.create(
            name=name,
            description=description,
            price=price,
            category_id=category_id,
            is_available=is_available
        )
        messages.success(request, 'Plat ajouté avec succès!')
        return redirect('menu_management')
    
    categories = Category.objects.all()
    return render(request, 'dashboard/add_dish.html', {'categories': categories})


@staff_required
def add_category(request):
    """Add new category"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        display_order = request.POST.get('display_order', 0)
        
        Category.objects.create(
            name=name,
            description=description,
            display_order=display_order
        )
        messages.success(request, 'Catégorie ajoutée avec succès!')
        return redirect('menu_management')
    
    return render(request, 'dashboard/add_category.html')


@staff_required
def edit_dish(request, dish_id):
    """Edit dish"""
    dish = get_object_or_404(Dish, id=dish_id)
    
    if request.method == 'POST':
        dish.name = request.POST.get('name')
        dish.description = request.POST.get('description')
        dish.price = request.POST.get('price')
        dish.category_id = request.POST.get('category')
        dish.is_available = request.POST.get('is_available') == 'on'
        dish.save()
        messages.success(request, 'Plat modifié avec succès!')
        return redirect('menu_management')
    
    categories = Category.objects.all()
    return render(request, 'dashboard/edit_dish.html', {'dish': dish, 'categories': categories})


@staff_required
def delete_dish(request, dish_id):
    """Delete dish"""
    dish = get_object_or_404(Dish, id=dish_id)
    dish.delete()
    messages.success(request, 'Plat supprimé avec succès!')
    return redirect('menu_management')


@staff_required
@require_http_methods(["POST"])
def delete_order(request):
    """Delete order API"""
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        
        order = Order.objects.get(order_id=order_id)
        order.delete()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
