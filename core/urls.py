from django.urls import path
from . import views
from .views import send_career_application

urlpatterns = [
    path('home/<slug:hotel_slug>/contact', views.hotel_contact_view, name='contact-page'),
    path('home/<slug:hotel_slug>/about', views.about_page, name='about-page'),
    path('home/<slug:hotel_slug>/faqs/', views.hotel_faqs, name='faqs-page'),
    path('home/<slug:hotel_slug>/careers/', views.careers_page, name='careers-page'),
    path('home/<slug:hotel_slug>/careers/<slug:career_slug>/', views.career_detail, name='career-detail'),
    path('careers/apply/', send_career_application, name='career-apply'),
]

