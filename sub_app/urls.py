from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main_home' ),
    path( 'journal/', views.journal, name='main_journal' ),
    path('analysis/', views.analysis, name='main_analysis' ),
]
