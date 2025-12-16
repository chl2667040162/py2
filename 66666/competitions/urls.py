from django.urls import path
from . import views

urlpatterns = [
    path('', views.competition_list, name='competition_list'),
    path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('competition/new/', views.competition_create, name='competition_create'),
    path('competition/<int:pk>/', views.competition_detail, name='competition_detail'),
    path('competition/<int:pk>/edit/', views.competition_edit, name='competition_edit'),
    path('competition/<int:pk>/delete/', views.competition_delete, name='competition_delete'),
    path('competition/<int:pk>/register/', views.register_participant, name='register_participant'),
]