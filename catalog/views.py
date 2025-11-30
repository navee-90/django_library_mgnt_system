from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import Book, Borrow, Member, Cart, Wishlist, Order
from .forms import BorrowForm

# ------------------ HOME PAGE ------------------
def index(request):
    books = Book.objects.all()
    paginator = Paginator(books, 10)
    page = request.GET.get('page')
    books_page = paginator.get_page(page)
    return render(request, 'catalog/index.html', {'books': books_page})

# ------------------ SIGNUP ------------------
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created and logged in successfully!")
            return redirect('catalog:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# ------------------ SIGNIN ------------------
def signin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('catalog:index')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'registration/signin.html')
    return render(request, 'registration/signin.html')

# ------------------ SIGNOUT ------------------
@login_required
def signout_view(request):
    logout(request)
    messages.success(request, "You have signed out successfully.")
    return redirect('catalog:index')

# ------------------ BOOK DETAIL ------------------
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    in_cart = in_wishlist = False
    if request.user.is_authenticated:
        in_cart = Cart.objects.filter(user=request.user, book=book).exists()
        in_wishlist = Wishlist.objects.filter(user=request.user, book=book).exists()
    return render(request, 'catalog/book_detail.html', {
        'book': book,
        'in_cart': in_cart,
        'in_wishlist': in_wishlist,
    })

# ------------------ BORROW BOOK ------------------
@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    member, _ = Member.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            if book.available_copies <= 0:
                form.add_error(None, "No copies available")
            else:
                borrow = form.save(commit=False)
                borrow.member = member
                borrow.book = book
                book.available_copies -= 1
                book.save()
                borrow.save()
                return redirect('catalog:index')
    else:
        form = BorrowForm(initial={'book': book})
    return render(request, 'catalog/borrow_form.html', {'form': form, 'book': book})

# ------------------ CART ------------------
@login_required
def cart_page(request):
    items = Cart.objects.filter(user=request.user)
    return render(request, 'catalog/cart_page.html', {'items': items})

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('catalog:cart')

@login_required
def remove_from_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    Cart.objects.filter(user=request.user, book=book).delete()
    return redirect('catalog:cart')

# ------------------ WISHLIST ------------------
@login_required
def wishlist_page(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'catalog/wishlist_page.html', {'items': items})

@login_required
def add_to_wishlist(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    Wishlist.objects.get_or_create(user=request.user, book=book)
    return redirect('catalog:wishlist_page')

@login_required
def remove_from_wishlist(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    Wishlist.objects.filter(user=request.user, book=book).delete()
    return redirect('catalog:wishlist_page')

# ------------------ ORDER PAGE ------------------
@login_required
def order_page(request):
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        Order.objects.create(user=request.user, book=item.book, quantity=item.quantity)
        if item.book.available_copies >= item.quantity:
            item.book.available_copies -= item.quantity
            item.book.save()
    cart_items.delete()
    return render(request, 'catalog/order_page.html')
