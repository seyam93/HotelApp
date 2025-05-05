from django.urls import path
from . import views

urlpatterns = [
    path('home/<slug:hotel_slug>/team/', views.team_list, name='team-list-page'),
    path('home/<slug:hotel_slug>/team/<int:manager_id>/', views.team_detail, name='team-detail-page'),
]