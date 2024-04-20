from django.urls import path
from . import views

urlpatterns = [
    path('linker/companies/', views.list_companies, name='list_companies'),
    path('linker/company-add/', views.add_company, name='add_company'),
    path('linker/<str:id>/', views.detail_company, name='detail_company'),
    path('linker/<str:id>/delete/', views.delete_company, name='delete_company'),
    path('<slug:short_link>', views.redirect_link, name='redirect'),
    
]
