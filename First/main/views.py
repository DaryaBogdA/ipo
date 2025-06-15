import json, os
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from .models import Product, Producer, ProductCategory, Cart, CartItem
from django.views.generic import DetailView
import tempfile
from django.core.mail import EmailMessage
from openpyxl import Workbook

def index(request):
    return render(request, 'main/home.html')


def about_i(request):
    return render(request, 'main/about_i.html')


def about_shop(request):
    return render(request, 'main/about_shop.html')


def load_json_data():
    json_path = os.path.join(settings.BASE_DIR, "static", "main", "json", "dump.json")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    skills = [
        {
            "id": item["pk"],
            "title": item["fields"]["title"],
            "code": item["fields"]["code"],
            "desc": item["fields"]["desc"],
            "searchtag": item["fields"]["searchtag"]
        }
        for item in data if item.get("model") == "data.skill"
    ]

    return skills


def spec(request):
    data = load_json_data()
    return render(request, "main/qualification.html", {"skills": data})


def skill_detail(request, skill_id):
    skills = load_json_data()
    skill = next((s for s in skills if s["id"] == skill_id), None)
    return render(request, "main/skill_detail.html", {"skill": skill})


def product_list(request):
    category_id = request.GET.get("category")
    producer_id = request.GET.get("producer")
    search_query = request.GET.get("search")

    products = Product.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)

    if producer_id:
        products = products.filter(producer_id=producer_id)

    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(text__icontains=search_query))

    context = {
        "products": products,
        "categories": ProductCategory.objects.all(),
        "producers": Producer.objects.all(),
    }

    return render(request, "main/product_list.html", context)


class NewsDetailView(DetailView):
    model = Product
    template_name = 'main/product_detail.html'
    context_object_name = 'product'


@login_required(login_url='login')
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.select_related('product').all()
    total_price = cart.total_price()

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'main/cart.html', context)


def registration(request):
    save = {}
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        save.update({
            'username': username,
            'password': password,
            'confirm_password': confirm_password,
        })

        if len(username) < 2 or len(username) > 32:
            messages.error(request, 'Имя пользователя от 2 до 32 символов')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
        elif password != confirm_password:
            messages.error(request, 'Пароли не совпадают')
        elif len(password) < 8 or len(password) > 32:
            messages.error(request, 'Пароль от 8 до 32 символов')
        else:

            user = User.objects.create_user(
                username=username,
                password=password,
            )

            login(request, user)
            return redirect('home')

    return render(request, 'main/registration.html', save)


@login_required(login_url='login')
def add_to_cart(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)

    total_reserved = CartItem.objects.filter(product=product).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    if total_reserved >= product.count:
        messages.error(request, f"«{product.name}» закончился.")
        return redirect(request.META.get('HTTP_REFERER', 'catalog'))

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    cart_item.quantity += 1
    cart_item.save()

    return redirect(request.META.get('HTTP_REFERER', 'catalog'))


@login_required(login_url='login')
def remove_from_cart(request, item_id):
    cart = Cart.objects.get(user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()

    return redirect('cart_view')


@login_required(login_url='login')
def update_cart_item(request, item_id):
    cart = Cart.objects.get(user=request.user)

    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product = item.product
    stock = product.count

    total_reserved = (
            CartItem.objects
            .filter(product=product)
            .aggregate(total=Sum('quantity'))['total']
            or 0
    )

    action = request.POST.get('action')
    if action == 'increase':
        if total_reserved >= stock:
            messages.error(request, f"Нельзя увеличить «{product.name}»: товар закончился на складе.")
        else:
            item.quantity += 1
            item.save()

    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
            messages.info(request, f"«{product.name}» удалён из корзины.")

    return redirect('cart_view')


@login_required(login_url='login')
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cart_items.select_related('product').all()

    if request.method == 'POST':
        address = request.POST.get('address', '').strip()
        email_to = request.POST.get('email', '').strip()
        if not email_to:
            messages.error(request, "Пожалуйста, укажите email для получения чека.")
            return render(request, 'main/checkout.html', {'cart_items': cart_items})

        wb = Workbook()
        ws = wb.active
        ws.title = "Чек"
        ws.append(["Товар", "Количество", "Цена", "Итого"])

        total_price = 0
        for item in cart_items:
            total = item.quantity * item.product.price
            ws.append([item.product.name, item.quantity, item.product.price, total])
            total_price += total
        ws.append(["", "", "Итого:", total_price])

        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
            wb.save(tmp.name)
            tmp.seek(0)
            excel_data = tmp.read()

        try:
            email = EmailMessage(
                subject="Ваш чек",
                body=f"Спасибо за заказ! \n Доставка по адресу: {address}",
                from_email=settings.EMAIL_HOST_USER,
                to=[email_to],
            )
            email.attach('order.xlsx', excel_data, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            email.send()

            cart.cart_items.all().delete()
            messages.success(request, f"Заказ успешно оформлен! Чек отправлен на почту: {email_to}")
            return redirect('catalog')
        except Exception as e:
            messages.error(request, f"Произошла ошибка: {str(e)}")
            return render(request, 'main/checkout.html', {'cart_items': cart_items})

    return render(request, 'main/checkout.html', {
        'cart_items': cart_items,
    })






















