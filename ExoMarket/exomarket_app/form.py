from django import forms
from .models import CustomUser, Item, Cart, CartItem
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, widget=forms.RadioSelect())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False  # All fields are not required by default
        
    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "password1", "password2", "phone_number", "role")
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "", "class": "form-control"}),
            "email": forms.EmailInput(attrs={"placeholder": "", "class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "(optional)", "class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"placeholder": "Enter your password", "class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"placeholder": "Confirm your password", "class": "form-control"}),
        }
        help_texts = {
            'username': '',  # Remove the help text for username
            'password1': None,
            'password2': None,
        }

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False  # Making fields non-required by default

class UserUpdateForm(UserChangeForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, widget=forms.RadioSelect())
    
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "phone_number", "role"]

class ItemCreationForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'categories', 'image', 'availability']
        widgets = {
            'name': forms.TextInput(attrs={"placeholder": "Item name", "class": "form-control"}),
            'description': forms.Textarea(attrs={"placeholder": "Item description", "class": "form-control"}),
            'price': forms.NumberInput(attrs={"placeholder": "Item price", "class": "form-control"}),
            'categories': forms.Select(attrs={"class": "form-control"}),
            'image': forms.ClearableFileInput(attrs={"class": "form-control"}),
            'availability': forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['item', 'quantity']
        widgets = {
            'item': forms.Select(attrs={"class": "form-control"}),
            'quantity': forms.NumberInput(attrs={"min": 1, "class": "form-control"}),
        }

class CartForm(forms.ModelForm):
    # For adding items to the cart
    class Meta:
        model = Cart
        fields = ['items']
        widgets = {
            'items': forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        }

class SearchForm(forms.Form):
    category = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    user = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))



class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)