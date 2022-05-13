from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main_home' ),
    path( 'journal/', views.journal, name='main_journal' ),
    path('analysis/', views.analysis, name='main_analysis' ),
    path('analysis_2/', views.analysis_2, name='main_analysis_2' ),
    path('analysis_3/', views.analysis_3, name='main_analysis_3' ),
    path('analysis_4/', views.analysis_4, name='main_analysis_4' ),
    path('analysis_5/', views.analysis_5, name='main_analysis_5' ),

]
