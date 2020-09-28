from django.shortcuts import render
from zebi.functions import check_clearance, get_default_arguments, check_uuid
from django.contrib.auth.decorators import login_required
from .models import Book
from django.http import Http404, FileResponse
from django.shortcuts import get_object_or_404


@login_required
def home(request):
    all_books = Book.objects.all().filter(clearance__lte=request.user.profile.clearance)
    arguments = {**get_default_arguments(request), 'books': all_books}
    return render(request, 'library/home.html', arguments)


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
