from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message_text = request.POST.get("message", "").strip()

        if not (name and email and subject and message_text):
            messages.error(request, "Please fill all fields.")
            return redirect('contact')

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message_text
        )

        messages.success(request, "Thank you! Your message has been sent ✅")
        return redirect('contact')

    return render(request, "main/contact.html")
