from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .validators import validate_phone_number, validate_price, validate_quantity, validate_forbidden_words
from PIL import Image


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("WI", "Wizard"),
        ("WA", "Warrior")
    ]
    coins = models.IntegerField(default=1000)
    phone_number = models.CharField(max_length=15, blank=True, null=True, validators=[validate_phone_number])
    role = models.CharField(choices=ROLE_CHOICES, max_length=10)
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ['username']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self) -> str:
        return self.username


class Item(models.Model):
    CATEGORY_CHOICES = [
        ("W", "Weapon"),
        ("A", "Armor"),
        ("S", "Spellbook")
    ]
    name = models.CharField(max_length=255, validators=[validate_forbidden_words])
    description = models.TextField(validators=[validate_forbidden_words])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_price])
    seller = models.ForeignKey(CustomUser, related_name='items_for_sale', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    availability = models.BooleanField(default=True)
    categories = models.CharField(choices=CATEGORY_CHOICES, max_length=50)

    def __str__(self) -> str:
        return f"{self.name} and {self.price}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                img = img.resize((300, 300))
                img.save(self.image.path)

    class Meta:
        ordering = ['name']
        verbose_name = 'Item'
        verbose_name_plural = 'Items'


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField(Item, related_name='carts', blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self) -> str:
        return f"{self.user.username}'s cart: {[item for item in self.items]}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[validate_quantity])

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'


class Transaction(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transactions', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, related_name='sales', on_delete=models.CASCADE, null = True, blank = True)  # New Seller
    quantity = models.IntegerField()
    total_amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.buyer.username} purchased {self.item.name} from {self.seller.username} for {self.total_amount} coins"

