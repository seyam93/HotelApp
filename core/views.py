from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from core.models import ContactMessage, Partner, FAQ, Career, CareerApplication
from core.forms import CareerApplicationForm
from hotels.models import Hotel, Review, HotelPageBanner, HotelVideoBanner
from hotels.models import Hotel, HotelService
from staff.models import Manager
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.mail import send_mail

# Contact Page Function
def hotel_contact_view(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    image_banner = HotelPageBanner.objects.filter(hotel=hotel, page='contact').first()
    video_banner = HotelVideoBanner.objects.filter(hotel=hotel, page='contact').first()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        email_body = f"""
Hotel: {hotel.name}

Name: {name}
Email: {email}
Phone: {phone}
Subject: {subject or 'No subject'}

Message:
{message}
"""

        try:
            send_mail(
                subject=f"[{hotel.name}] Contact Form: {subject or 'No Subject'}",
                message=email_body,
                from_email='no-reply@yourdomain.com',
                recipient_list=['info@triumphhotel.com'],
                fail_silently=False,
            )
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            messages.success(request, "Your message has been sent.")
        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)}, status=500)
            messages.error(request, "Something went wrong.")

        return redirect('contact-page', hotel_slug=hotel.slug)  

    return render(request, 'hotels/contact.html', {'hotel': hotel, 'banner': image_banner, 'video_banner': video_banner})

# About Page Function
def about_page(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)

    image_banner = HotelPageBanner.objects.filter(hotel=hotel, page='about').first()
    video_banner = HotelVideoBanner.objects.filter(hotel=hotel, page='about').first()

    context = {
        'hotel': hotel,
        'banner': image_banner,          # ✅ only image banner goes here
        'video_banner': video_banner,    # ✅ only video banner here
        'partners': Partner.objects.filter(hotel=hotel),
        'managers': Manager.objects.filter(hotel=hotel),
        'services': HotelService.objects.filter(hotel=hotel, is_active=True),
        'reviews': Review.objects.filter(hotel=hotel).order_by('-created_at'),
        'amenity_services': HotelService.objects.filter(hotel=hotel, is_active=True),
    }
    return render(request, 'hotels/about.html', context)

# FAQs page function
def hotel_faqs(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    faqs = hotel.faqs.all()  # using the related_name='faqs' from the FAQ model
    image_banner = HotelPageBanner.objects.filter(hotel=hotel, page='faqs').first()
    video_banner = HotelVideoBanner.objects.filter(hotel=hotel, page='faqs').first()
    return render(request, 'core/hotel_faqs.html', {
        'hotel': hotel,
        'faqs': faqs,
        'banner': image_banner,
        'video_banner': video_banner,
    })

# Careers page function
def careers_page(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    careers = hotel.careers.all()  # Use related_name from your ForeignKey
    image_banner = HotelPageBanner.objects.filter(hotel=hotel, page='careers').first()
    video_banner = HotelVideoBanner.objects.filter(hotel=hotel, page='careers').first() 

    return render(request, 'core/hotel_careers.html', {
        'hotel': hotel,
        'careers': careers,
        'banner': image_banner,
        'video_banner': video_banner,
    })

# Career Application Form
@require_POST
@csrf_exempt  # optional if using AJAX with CSRF token correctly
def send_career_application(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    message = request.POST.get('message')
    job_title = request.POST.get('job_title')
    resume = request.FILES.get('resume')

    subject = f"New Career Application for: {job_title}"
    body = (
        f"Job Title: {job_title}\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Phone: {phone}\n\n"
        f"Message:\n{message}"
    )

    to_email = 'info@triumphhotel.com'  # 🔴 replace with your real HR or notification email

    email_msg = EmailMessage(subject, body, to=[to_email])

    if resume:
        email_msg.attach(resume.name, resume.read(), resume.content_type)

    try:
        email_msg.send()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    