from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Cart, CustomUser, CartItem, Transaction
from django.core.paginator import Paginator
from django.views.generic import ListView,TemplateView,DetailView,CreateView,FormView,RedirectView,UpdateView
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.urls import reverse
from .form import CustomUserCreationForm,ItemCreationForm,CustomAuthenticationForm,UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants as message_constants
from django.core.paginator import Paginator
from django.db.models import Q

from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Sum
from collections import defaultdict

from django.core.mail import send_mail
from .form import ContactForm
from django.conf import settings



def item_list(request):
    items = Item.objects.all()
    paginator = Paginator(items, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'exomarket_app/item_list.html', {'items': items})

@login_required
def cart_list(request):
    carts = Cart.objects.filter(user=request.user) 
    return render(request, 'exomarket_app/cart_list.html', {'carts': carts})

    
class UsersListView(ListView):
    model = CustomUser
    template_name="exomarket_app/users.html"    
    context_object_name = "users" 
    
#class HomePageView(TemplateView):
    #template_name="exomarket_app/home.html"    
    
class UserDetailView(DetailView):
    model = CustomUser
    template_name = "exomarket_app/profile.html"
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filter active transactions for the user
        user_transactions = Transaction.objects.filter(
            Q(buyer=self.object) | Q(seller=self.object),
            is_active=True
        )

        # Aggregate transactions by item and calculate total quantity
        aggregated_transactions = defaultdict(lambda: {'total_quantity': 0, 'item': None})
        
        for transaction in user_transactions:
            item = transaction.item
            if aggregated_transactions[item.id]['item'] is None:
                aggregated_transactions[item.id]['item'] = item  # Save the item info (name, image)
            
            aggregated_transactions[item.id]['total_quantity'] += transaction.quantity

        # Convert the aggregated transactions to a list for the template
        aggregated_transactions = list(aggregated_transactions.values())

        # Add aggregated transactions to the context
        context['aggregated_transactions'] = aggregated_transactions

        return context
    
    
class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "exomarket_app/register.html"
    success_url = reverse_lazy("home")

class UserLoginView(FormView):
    form_class = CustomAuthenticationForm
    template_name = "exomarket_app/login.html"
    success_url = reverse_lazy("home")

    def form_valid(self,form):
        if form.cleaned_data.get("username") and form.cleaned_data.get("password"):
            user = form.get_user()
            if user:  # Ensure the user exists
                login(self.request, user)
        else:
            return self.form_invalid(form)  # Treat as invalid if empty data is present
        return super().form_valid(form)
    
    
class UserLogoutView(LoginRequiredMixin,RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        print(self.request.user)
        return super().get(request, *args, **kwargs)    
    
    
class ItemCreateView(LoginRequiredMixin,CreateView):
    form_class = ItemCreationForm
    template_name="exomarket_app/create_item.html"

    def form_valid(self, form):
        form.instance.seller = self.request.user 
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('item_list')






@login_required
def checkout(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id, user=request.user)
    
   
    total_price = sum(cart_item.item.price * cart_item.quantity for cart_item in cart.cart_items.all())
    
    if request.user.coins < total_price:
        messages.error(request, "You don't have enough coins to complete this transaction!")
        return redirect('cart_list')  
    
    request.user.coins -= total_price
    request.user.save()

    for cart_item in cart.cart_items.all():
        seller = cart_item.item.seller  
        total_item_price = cart_item.item.price * cart_item.quantity
        seller.coins += total_item_price 
        seller.save()

        Transaction.objects.create(
            buyer=request.user,
            item=cart_item.item,
            seller=seller,
            quantity=cart_item.quantity,
            total_amount=total_item_price
        )

    cart.cart_items.all().delete()

   
    messages.success(request, f"Transaction successful! The new item was added to your inventory. You spent {total_price} coins.")
    return redirect('item_list')  



@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item = CartItem.objects.filter(cart=cart, item=item).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
        messages.info(request, f"The quantity of the item '{item.name}' has been increased by 1.")
    else:
        CartItem.objects.create(cart=cart, item=item, quantity=1)
        messages.success(request, f"The item '{item.name}' has been added to your cart.")

    return redirect('item_list')




@login_required
def delete_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete() 
    return redirect('cart_list')  




def home(request):
    if request.user.is_authenticated:
        transactions = Transaction.objects.filter(
            Q(buyer=request.user) | Q(seller=request.user),
            is_active=True  
        ).order_by('-date')  

        paginator = Paginator(transactions, 10)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, 'exomarket_app/home.html', {
            'page_obj': page_obj,
        })
    else:
        return render(request, 'exomarket_app/home.html')


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Your account has been successfully deleted.")
        return HttpResponseRedirect(reverse("home"))
    
    
    
    
@login_required
def delete_item_from_market(request, item_id):
    item = get_object_or_404(Item, id=item_id, seller=request.user)
    if request.method == "POST":
        item.delete()
        messages.success(request, f"The item '{item.name}' has been removed from the market.")
        return redirect('profile', username=request.user.username)
    
    
    
@login_required
def confirm_delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        logout(request)  
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')  
    return render(request, 'exomarket_app/confirm_delete_account.html')
    
    
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'exomarket_app/password_change.html'  
    success_url = reverse_lazy('home')  
    
    
    
    
    
def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

           #no real email!!! 
            print(f"Kontaktformular abgeschickt: {name} ({email}) sagte: {message}")

            return redirect('contact_success')
    else:
        form = ContactForm()

    return render(request, 'contact/contact_us.html', {'form': form})

def contact_success(request):
    return render(request, 'contact/success.html')




class UserUpdateView(UpdateView):
    model = CustomUser
    fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'role']
    template_name = 'exomarket_app/profile_update.html'
    
    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(CustomUser, username=username)
    
    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.object.username})
