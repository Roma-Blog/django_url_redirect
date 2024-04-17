from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('linker/companies/', views.list_companies, name='list_companies'),
    path('linker/company-add/', views.add_company, name='add_company'),
]
