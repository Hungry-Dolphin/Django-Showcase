from django.shortcuts import render, redirect
from zebi.functions import check_clearance, get_default_arguments, check_uuid
from django.contrib.auth.decorators import login_required
from .models import Book, Comments
from .forms import CommentForm, BookForm
from django.http import Http404, FileResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages


@login_required
def home(request):
    all_books = Book.objects.all().filter(clearance__lte=request.user.profile.clearance)
    arguments = {**get_default_arguments(request), 'books': all_books}
    return render(request, 'library/home.html', arguments)


@login_required()
def book_details(request, book):
    if not check_uuid(book):
        raise Http404

    book = get_object_or_404(Book, id=book)
    if check_clearance(request, book):
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                Comments(
                    user=request.user,
                    content=form.cleaned_data.get('content'),
                    book=book
                ).save()
                return redirect(request.path_info)

        comments = Comments.objects.all().filter(book=book)
        arguments = {**get_default_arguments(request), 'book': book, 'comments': comments, 'form': CommentForm()}
        return render(request, 'library/book.html', arguments)
    else:
        return Http404


@login_required
def upload_pdf(request):
    if request.method == 'POST':
        form = BookForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            return redirect(home)
        else:
            messages.error(request, "Please correct the errors below")
            arguments = {**get_default_arguments(request), 'form': form}
            return render(request, 'library/upload.html', arguments)

    arguments = {**get_default_arguments(request), 'form': BookForm(request.user)}
    return render(request, 'library/upload.html', arguments)


@login_required
def pdf(request, book):
    if not check_uuid(book):
        raise Http404

    book = get_object_or_404(Book, id=book)
    if check_clearance(request, book):
        try:
            return FileResponse(open(f'{book.pdf}', 'rb'), content_type='application/pdf')
        except FileNotFoundError:
            raise Http404()
    else:
        return Http404
