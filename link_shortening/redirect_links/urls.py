from django.urls import path
from . import views

urlpatterns = [
    path('linker/companies/', views.list_companies, name='list_companies'),
    path('linker/company-add/', views.add_company, name='add_company'),
    path('<slug:short_link>', views.redirect_link, name='redirect'),
]
