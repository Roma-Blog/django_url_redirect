from django.shortcuts import redirect, render
from .forms import CompaniesForm
from .models import Companies, Sesions
import random

# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[-1].strip()
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip

def generate_short_link() -> str:
    char = ['a','b','c','d','f','g','h','i','j',
        'k','l','m','n','o','p','q','r','s',
        't','u','v','w','x','y','z','1','2',
        '3','4','5','6','7','8','9','0','-']
    not_unique = True

    while not_unique:
        unique_ref = ''.join(random.choices(char, k=10))
        if not Companies.objects.filter(short_link = unique_ref):
            not_unique = False
    return unique_ref

def redirect_link(request, short_link):
    ip_user = request.META.get('HTTP_X_FORWARDED_FOR')
    if not ip_user:
        ip_user = request.META.get('REMOTE_ADDR')

    company = Companies.objects.get(short_link = short_link)
    Sesions.objects.create(
        id_company = company.id,
        user_id = 1,
        ip_user = ip_user,
        browser = request.META.get('HTTP_USER_AGENT'),
        city = 'Moscva'
    )

    return redirect(company.link)

def list_companies(request):
    return render(request, 'redirect_links/list_companies.html')

def add_company(request):
    
    if request.method == 'POST':
        company = Companies.objects.all()
        form = CompaniesForm(request.POST)
        if form.is_valid():
            Companies.objects.create(name = form.cleaned_data['name'], link = form.cleaned_data['link'], short_link = generate_short_link())
            return redirect('list_companies')
    else:
        form = CompaniesForm()

    context = {
        'form': form
    }
    return render(request, 'redirect_links/add_company.html', context)