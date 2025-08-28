from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required, user_passes_test
from contactform.models import ContactMessage
from accounts.models import CustomUser
from books.models import Book
from request.models import BookRequest
from accounts.forms import BookForm 
from notifications.models import Notification


User = get_user_model()

def signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        father_name = request.POST.get('father_name')
        department = request.POST.get('department')
        university_email = request.POST.get('university_email')
        whatsapp_number = request.POST.get('whatsapp_number')
        university_roll_no = request.POST.get('university_roll_no')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Basic validation
        if not all([full_name, father_name, department, university_email, whatsapp_number, university_roll_no, password1, password2]):
            messages.error(request, "Please fill out all fields.")
            return render(request, 'accounts/signup.html')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/signup.html')

        # Check if user or email or roll no already exists
        if User.objects.filter(university_email=university_email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'accounts/signup.html')

        if User.objects.filter(university_roll_no=university_roll_no).exists():
            messages.error(request, "Roll number already registered.")
            return render(request, 'accounts/signup.html')

        # Create user
        user = User.objects.create_user(
            full_name=full_name,
            father_name=father_name,
            department=department,
            university_email=university_email,
            whatsapp_number=whatsapp_number,
            university_roll_no=university_roll_no,
            password=password1
        )
        user.save()

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')  # Make sure you have a login URL named 'login'

    return render(request, 'main/auth.html')





# loginnnnnnnnnnnnnn


User = get_user_model()

# def user_login(request):
#     if request.method == 'POST':
#         email = request.POST.get('university_email')  # same as your input name
#         password = request.POST.get('password')

#         user = authenticate(request, university_email=email, password=password)

#         if user is not None:
#             login(request, user)

#             # Redirect based on role
#             if user.is_staff:  # Admin
#                 return redirect('admin_dashboard')  # URL name for admin dashboard
#             else:
#                 return redirect('user_dashboard')  # URL name for user dashboard

#         else:
#             messages.error(request, "Invalid email or password.")

#     return render(request, 'main/auth.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("university_email")  # must match your login form input name
        password = request.POST.get("password")       # must match your login form input name

        user = authenticate(request, username=email, password=password)  # username= is correct here
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

    return render(request, 'main/auth.html')


def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout




@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    # Dynamic stats
    total_books = Book.objects.count()
    pending_requests = BookRequest.objects.filter(status='pending').count()
    approved_requests = BookRequest.objects.filter(status='approved').count()
    
    # Pending requests for table
    requests = BookRequest.objects.filter(status='pending').order_by('-created_at')

    context = {
        'total_books': total_books,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'requests': requests,
    }

    return render(request, "main/admin_dashboard.html", context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def approve_request(request, pk):
    book_request = get_object_or_404(BookRequest, pk=pk)
    book_request.status = 'approved'
    book_request.save()
    return redirect('admin_dashboard')


@login_required
@user_passes_test(lambda u: u.is_staff)
def reject_request(request, pk):
    book_request = get_object_or_404(BookRequest, pk=pk)
    book_request.status = 'rejected'
    book_request.save()
    return redirect('admin_dashboard')









def user_dashboard(request):
    # user requests
    user_requests = BookRequest.objects.filter(requester=request.user)
    notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()

    # user uploaded books
    user_books = Book.objects.filter(uploader=request.user)

    return render(request, 'main/user_dashboard.html', {
        "user_requests": user_requests,
        "uploaded_books": user_books,
        "notifications_count": notifications_count,
    })



  

@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, uploader=request.user)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Your book has been updated successfully.")
            return redirect('user_dashboard')
    else:
        form = BookForm(instance=book)

    return render(request, 'main/edit_book.html', {'form': form, 'book': book})


@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, uploader=request.user)
    if request.method == 'POST':
        book.delete()
        messages.success(request, "Your book has been deleted successfully.")
        return redirect('user_dashboard')
    return render(request, 'main/confirm_delete.html', {'book': book})