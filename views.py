from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required 
from contactform.models import ContactMessage
from accounts.models import CustomUser
from books.models import Book
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from request.models import BookRequest
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages



# Create your views here.
from django.shortcuts import render

import random

# global variable rotation ke liye
current_offset = 0  

def home(request):
    global current_offset
    
    # ----- OPTION 1: Rotation (Batch System) -----
    # sab books lo
    all_books = list(Book.objects.all())
    batch_size = 8

    # agar koi book hai
    if all_books:
        # rotation ke liye slice nikalna
        books = all_books[current_offset:current_offset + batch_size]
        # agar list khali ho gayi to start se le lo
        if not books:
            current_offset = 0
            books = all_books[current_offset:current_offset + batch_size]

        # next time ke liye offset update karna
        current_offset += batch_size
    else:
        books = []

    # ----- OPTION 2: Random 8 Books -----
    # sirf neeche ki line ko uncomment karo agar random chahiye
    # books = Book.objects.order_by('?')[:8]

    return render(request, "main/index.html", {"books": books})




def about(request):
    return render(request,"main/about.html")

# def contact(request):
#     return render(request,"main/contact.html")







def browsebooks(request):
    books = Book.objects.all().order_by("-upload_date")

    # Filters
    category = request.GET.get("category")
    condition = request.GET.get("condition")
    search = request.GET.get("search")

    if category and category != "all":
        books = books.filter(category=category)

    if condition and condition != "All":
        books = books.filter(condition=condition)

    if search:
        books = books.filter(
            Q(title__icontains=search) |
            Q(author__icontains=search) |
            Q(genre__icontains=search) |
            Q(description__icontains=search) |
            Q(language__icontains=search)
        )

    # Pagination (6 books per page)
    paginator = Paginator(books, 6)
    page_number = request.GET.get("page")
    books_page = paginator.get_page(page_number)

    context = {"books": books_page}
    return render(request, "main/browse_page.html", context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "main/book_detail.html", {"book": book})





@login_required
def my_listings(request):
    # current user ki books filter karenge
    books = Book.objects.filter(uploader=request.user)
    return render(request, "main\mylisting.html", {"books": books})

# @login_required
# def addbook(request):
#     return render(request,"main/add_book.html")



@login_required
def my_requests(request):
    requests_list = BookRequest.objects.filter(requester=request.user).select_related("book")
    return render(request, "main/my_requests.html", {"requests": requests_list})




def manage_user(request):
    # ✅ Show all registered users
    all_users = CustomUser.objects.all().order_by('-university_roll_no')

    # ✅ Show all contact form submissions

    context = {
        'all_users': all_users,
    }
    
    return render(request, 'main/manage_user.html', context)


def manage_contacter(request):
    contact_messages = ContactMessage.objects.all().order_by('-date_sent')
    context = {
        'contact_messages': contact_messages
    }
    
    return render(request,"main/manage_contacter.html",context)



def respond_contact(request, contact_id):
    contact = get_object_or_404(ContactMessage, id=contact_id)

    if request.method == "POST":
        response_text = request.POST.get("response")
        if response_text:
            # send email
            send_mail(
                subject=f"Response to your query: {contact.subject}",
                message=response_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[contact.email],
                fail_silently=False,
            )
            messages.success(request, f"Response sent to {contact.email}")
            return redirect("manage_contacter")  # apna url name daalna
    return render(request, "main/respond_contact.html", {"contact": contact})
    

def editprofile(request):
    return render(request,"main/edit_profile.html")



def password_reset(request):
    return render(request,"main/password_reset.html")

def FAQ_view(request):
    return render(request,"main/FAQ_S.html")


