from django.urls import path
from . import views
urlpatterns = [
    path("user/", views.list_book, name="user_view"),
    path("userbookdetail/<int:book_id>/", views.user_detail_view, name='details'),
    path('usersearch/', views.search_book, name='search'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='addtocart'),
    path('view_cart/', views.view_cart, name='viewcart'),
    path('increase/<int:item_id>', views.increase_quantity, name="increase_quantity"),
    path("decrease/<int:item_id>", views.decrease_quantity, name="decrease_quantity"),
    path("remove_cart/<int:item_id>", views.remove_cart, name="remove_cart"),
    path("create-checkout-session/", views.create_checkout_session, name='create_checkout_session'),
    path("success/", views.success, name='success'),
    path("cancel/", views.cancel, name='cancel')
]