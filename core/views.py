from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from core.models import ContactMessage, Partner, FAQ, Career, CareerApplication
from core.forms import CareerApplicationForm
from hotels.models import Hotel, Review
from hotels.models import Hotel, HotelService
from staff.models import Manager

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

# About Page Function
def about_page(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)

    partners = Partner.objects.filter(hotel=hotel)
    managers = Manager.objects.filter(hotel=hotel)
    services = HotelService.objects.filter(hotel=hotel, is_active=True)
    reviews = Review.objects.filter(hotel=hotel).order_by('-created_at')
    amenity_services = HotelService.objects.filter(hotel=hotel, is_active=True)

    context = {
        'hotel': hotel,
        'partners': partners,
        'managers': managers,
        'services': services,
        'reviews': reviews,
        'amenity_services': amenity_services,
    }
    return render(request, 'hotels/about.html', context)

# FAQs page function
def hotel_faqs(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    faqs = hotel.faqs.all()  # using the related_name='faqs' from the FAQ model
    return render(request, 'core/hotel_faqs.html', {
        'hotel': hotel,
        'faqs': faqs
    })

# Careers page function
def careers_page(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    careers = hotel.careers.all()  # Use related_name from your ForeignKey
    return render(request, 'core/hotel_careers.html', {
        'hotel': hotel,
        'careers': careers
    })

# Career_details page function & form submission
def career_detail(request, hotel_slug, career_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    career = get_object_or_404(Career, slug=career_slug, hotel=hotel)

    if request.method == 'POST':
        form = CareerApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.career = career
            application.save()
            # Optional: add success message
            return redirect('career-thank-you')  # or same page with success
    else:
        form = CareerApplicationForm()

    return render(request, 'core/career_detail.html', {
        'career': career,
        'form': form,
        'hotel': hotel
    })