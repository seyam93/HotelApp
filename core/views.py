from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from core.models import ContactMessage
from hotels.models import Hotel

def hotel_contact_view(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message,
            hotel=hotel
        )

        # (Optional) Store full message string for future email logic
        full_message = f"""
New contact form message from {hotel.name}

Name: {name}
Email: {email}
Phone: {phone}
Subject: {subject}

Message:
{message}
"""

        # TEMPORARILY DISABLED:
        # from django.core.mail import send_mail
        # send_mail(
        #     subject=f"[{hotel.name}] Contact Form: {subject or 'No Subject'}",
        #     message=full_message,
        #     from_email='no-reply@yourdomain.com',
        #     recipient_list=['info@triumphhotel.com'],
        #     fail_silently=False,
        # )

        messages.success(request, "Your message has been sent.")
        return redirect('hotel-contact', hotel_slug=hotel.slug)

    return render(request, 'hotels/contact.html', {'hotel': hotel})