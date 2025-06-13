"""
URL configuration for hotel_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import set_language
from hotels import views as hotel_views
from django.conf.urls import handler404
from django.shortcuts import render


urlpatterns = [
    path("admin/", admin.site.urls),
    path('set-language/', set_language, name='set_language'),
    path('', hotel_views.home, name='home-page'), # Home page
    path("", include("hotels.urls")),          # all hotel-related pages
    path("", include("restaurants.urls")),      # all restaurant-related pages
    path("", include("meeting_rooms.urls")),    # all meeting room-related pages
    path("", include("events.urls")),          # all event-related pages
    path("", include("core.urls")),            # all core-related pages
    path("", include("staff.urls")),            # all staff-related pages
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404_view
