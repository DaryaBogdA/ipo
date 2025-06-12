from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Producer(models.Model):
    name = models.CharField('Название',max_length=100)
    country = models.CharField('Страна',max_length=100)
    text = models.TextField('Описание', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Производители"

    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    name = models.CharField('Название', max_length=100)
    text = models.TextField('Описание', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Категории товаров"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField('Название', max_length=200)
    text = models.TextField('Описание')
    photo = models.ImageField('Фото товара', upload_to='products/')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    count = models.IntegerField('Количество на складе', validators=[MinValueValidator(0)])

    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="products")
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, related_name="products")

    class Meta:
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} ({self.producer.name})"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    def total_price(self):
        return sum(item.item_price() for item in self.cart_items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items", verbose_name="Корзина")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(
        verbose_name="Количество",
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name_plural = "Элементы корзины"

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"

    def item_price(self):
        return self.product.price * self.quantity

    def clean(self):
        if self.quantity > self.product.count:
            raise ValidationError(f"Нельзя добавить больше")



# login admin
#password admin_228

# asdf
# 1471asdf

# qwer
# 1471qwer

# tyui
# 1471tyui

# ghjk
# 1471ghjk