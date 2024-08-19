from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Book

from .forms import AuthorForm, BookForm


# Create your views here.

def createbook(request):
    books = Book.objects.all()

    if request.method == 'POST':
        form = BookForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('booklist')
    else:
        form = BookForm()
    return render(request, 'book.html', {'form': form, 'books': books})


def listBook(request):
    # to see all the book details in the home page
    books = Book.objects.all()

    paginator = Paginator(books, 2)
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)

    except EmptyPage:
        page = paginator.page(page_number.num_pages)

    # if you want to see the details in another page
    # {'books':books} context
    return render(request, 'listbook.html', {'books': books, 'page': page})


def detailView(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'detailsview.html', {'book': book})


def createAuthor(request):
    if request.method == 'POST':

        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('createbook')
    else:
        form = AuthorForm
    return render(request, 'author.html', {'form': form})


def updateBook(request, book_id):
    book = Book.objects.get(id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book, files=request.FILES)

        if form.is_valid():
            form.save()
        return redirect('/')
    else:
        form = BookForm(instance=book)
    return render(request, 'updatebook.html', {'form': form})


def deleteView(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('/')

    return render(request, 'deleteview.html', {'book': book})


def index(request):
    return render(request, 'base.html')


def Search_Book(request):
    query = None
    books = None

    if 'q' in request.GET:
        query = request.GET.get('q')
        books = Book.objects.filter(Q(title__icontains=query))
    else:
        books = []

    context = {
        'books': books,
        'query': query
    }
    return render(request, 'search.html', context)
