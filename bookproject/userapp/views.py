from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from bookapp.models import Book
from userapp.models import Cart, CartItem
from accounts.models import UserProfile
import stripe
from django.contrib.auth.decorators import login_required


def list_book(request):
    books = Book.objects.all()
    paginator = Paginator(books, 2)
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.get_page(page_number.num_pages)

    return render(request, 'user_book_list.html', {'books': books, 'page': page})


def user_detail_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'user_details_view.html', {'book': book})


def search_book(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(Q(title__icontains=query)) if query else []

    context = {
        'books': books,
        'query': query
    }
    return render(request, 'user_search.html', context)


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.quantity > 0:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        cart, created = Cart.objects.get_or_create(user=user_profile)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, book=book)

        if not item_created:
            cart_item.quantity += 1
        else:
            cart_item.quantity = 1
        cart_item.save()

        messages.success(request, "Book added to cart.")
    else:
        messages.error(request, "Book is out of stock.")
    return redirect("viewcart")


@login_required
def view_cart(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        cart, created = Cart.objects.get_or_create(user=user_profile)
        cart_items = cart.cartitem_set.all()
        total_price = sum(item.book.price * item.quantity for item in cart_items)
        total_items = sum(item.quantity for item in cart_items)

        context = {
            "cart_items": cart_items,
            "total_price": total_price,
            "total_items": total_items
        }

        return render(request, 'cart.html', context)
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile does not exist.')
        return redirect('login')


@login_required
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if cart_item.quantity < cart_item.book.quantity:
        cart_item.quantity += 1
        cart_item.save()
    else:
        messages.error(request, "Cannot add more items than available in stock.")

    return redirect("viewcart")


@login_required
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        messages.error(request, "Cannot have less than 1 item in the cart.")

    return redirect("viewcart")


@login_required
def remove_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect("viewcart")

@login_required
def create_checkout_session(request):
    cart_items = CartItem.objects.filter(cart__user__user=request.user)

    if cart_items:
        stripe.api_key = settings.STRIPE_SECRETE_KEY

        if request.method == 'POST':
            line_items = []
            for cart_item in cart_items:
                if cart_item.book:
                    line_item = {
                        'price_data': {
                            'currency': 'INR',
                            'unit_amount': int(cart_item.book.price * 100),
                            'product_data': {
                                'name': cart_item.book.title
                            },
                        },
                        'quantity': cart_item.quantity
                    }
                    line_items.append(line_item)
            if line_items:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('success')),
                    cancel_url=request.build_absolute_uri(reverse('cancel'))
                )
                return redirect(checkout_session.url, code=303)

    messages.error(request, 'No items in cart to checkout.')
    return redirect('viewcart')


@login_required
def success(request):
    # Retrieve the UserProfile for the current user
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Filter CartItem by the UserProfile instance
    cart_items = CartItem.objects.filter(cart__user=user_profile)

    # Process cart items
    for cart_item in cart_items:
        product = cart_item.book
        if product.quantity >= cart_item.quantity:
            product.quantity -= cart_item.quantity
            product.save()

    # Delete cart items
    cart_items.delete()

    return render(request, 'success.html')


def cancel(request):
    return render(request, 'cancel.html')

