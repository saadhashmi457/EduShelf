from django.shortcuts import render, redirect
from books.models import Book
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from request.models import BookRequest
from django.contrib import messages
from request.models import BookRequest
from notifications.models import Notification

@login_required
def upload_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        genre = request.POST.get("genre")
        category = request.POST.get("category")
        language = request.POST.get("language")
        condition = request.POST.get("condition")
        price = request.POST.get("price")
        description = request.POST.get("description")
        cover_image = request.FILES.get("cover_image")

        # Validation: Price required if category = sell
        if category == "sell" and not price:
            return render(request, "main/upload_book.html", {"error": "Price is required for Sell category."})

        # Save to database
        Book.objects.create(
            title=title,
            author=author,
            genre=genre,
            category=category,
            language=language,
            condition=condition,
            price=price if price else None,
            description=description,
            cover_image=cover_image,
            uploader=request.user
        )

        return redirect("Suceessmsg")  

    return render(request, "main/upload_book.html")

def Suceessmsg(request):
    return render(request,"main/success_messsageofupload.html")




def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    existing_request = None
    is_uploader = False

    if request.user.is_authenticated:
        # Check if current user is uploader
        if request.user == book.uploader:
            is_uploader = True
        else:
            # Check if current user already requested this book
            existing_request = BookRequest.objects.filter(
                requester=request.user,
                book=book
            ).first()

    context = {
        "book": book,
        "existing_request": existing_request,
        "is_uploader": is_uploader,
    }
    return render(request, "main/book_detail.html", context)


@login_required
def request_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.user == book.uploader:
        messages.error(request, "⚠️ You cannot request your own uploaded book.")
        return redirect("book_detail", book_id=book.id)

    if request.method == "POST":
        existing_request = BookRequest.objects.filter(
            requester=request.user,
            book=book
        ).first()

        if existing_request:
            messages.warning(request, "⚠️ You already requested this book.")
        else:
            # Create new request
            BookRequest.objects.create(
                requester=request.user,
                book=book,
                status="pending"
            )

            # ✅ Add notification for uploader
            from notifications.models import Notification
            requester_name = getattr(request.user, "full_name", request.user.university_email)

            Notification.objects.create(
                user=book.uploader,
                book=book,
                message=f"📖 {requester_name} requested your book '{book.title}'."
            )


            messages.success(request, "✅ Your request has been sent successfully!")

    return redirect("book_detail", book_id=book.id)



def mark_notification_read(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect("user_dashboard")



