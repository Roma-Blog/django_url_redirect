from django.shortcuts import redirect, render
from .forms import CompaniesForm

def index(request):
    return redirect('https://google.com')

def list_companies(request):
    return render(request, 'redirect_links/list_companies.html')

def add_company(request):
    if request.method == 'POST':
        form = CompaniesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_companies')
    else:
        form = CompaniesForm()

    context = {
        'form': form
    }
    return render(request, 'redirect_links/add_company.html', context)