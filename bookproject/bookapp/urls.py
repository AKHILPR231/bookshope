from django.urls import path
from . import views

urlpatterns = [
    path("create-book/", views.createbook, name='createbook'),
    path("author/", views.createAuthor, name='author'),
    path('list/', views.listBook, name='booklist'),
    path('detailsview/<int:book_id>/', views.detailView, name='details'),
    path('updateview/<int:book_id>/', views.updateBook, name='updates'),
    path('deleteview/<int:book_id>/', views.deleteView, name='delete'),
    path('index/', views.index),
    path('search/', views.Search_Book, name='admin_search')
]
