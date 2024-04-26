from django.shortcuts import redirect, render
from django.http import Http404
from .forms import CompaniesForm
from .models import Companies, Sesions
from django.db.models import Avg, Max, Min, Sum
import random, requests, datetime

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

def get_city(ip):
    try:
        city = requests.get('http://ipwho.is/' + ip + '?lang=ru')
        return city.json()['city']
    except:
        return 'Неизвестно'


def redirect_link(request, short_link):

    try:
        company = Companies.objects.get(short_link = short_link)
    except Companies.DoesNotExist:
        raise Http404

    ip_user = request.META.get('HTTP_X_FORWARDED_FOR')
    if not ip_user:
        ip_user = request.META.get('REMOTE_ADDR')

    Sesions.objects.create(
        id_company = company,
        ip_user = ip_user,
        browser = request.META.get('HTTP_USER_AGENT'),
        city = get_city(ip_user)
    )

    # Генерация 1 000 000 сессий
    # date_now = datetime.datetime.now().date()
    # count_sesions = random.randint(1, 50) 
    # day = 0
    # for i in range(1000000):
    #     if count_sesions == 0:
    #         count_sesions = random.randint(1, 50) 
    #         day += 1

    #     Sesions.objects.create(
    #         id_company = company,
    #         ip_user = '127.{a}.{b}.{c}'.format(a = random.randint(0, 255), b = random.randint(0, 255), c = random.randint(0, 255)),
    #         browser = random.choice(['Chrome', 'Firefox', 'Safari', 'Opera', 'Edge']),
    #         city = random.choice(['Москва', 'Новосибирск','Барнаул','Иркутск','Владивосток','Тюмень','Кемерово','Санкт-Петербург']),
    #         data = date_now + datetime.timedelta(days = day)
    #     )
    #     count_sesions -= 1


    return redirect(company.link, permanent=True)

def list_companies(request):
    companies = Companies.objects.all()
    context = {
        'companies': companies
    }
    return render(request, 'redirect_links/list_companies.html', context)

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

def detail_company(request, id):
    data_beginning = None
    data_end = None

    if request.method == 'GET':
        if request.GET.get('beginning') and request.GET.get('end'):
            
            data_beginning = datetime.datetime(*list(map(int, request.GET.get('beginning').split('-')))).date()
            data_end = datetime.datetime(*list(map(int, request.GET.get('end').split('-')))).date()
    
    sesions = Sesions.objects.filter(id_company = id)
    company = Companies.objects.get(id = id)
    list_data = list(item.data for item in sesions)
    sesions_data: str = ''

    if not data_beginning and not data_end:
        data_beginning = list_data[0] - datetime.timedelta(days=6)
        data_end = list_data[0]

    count_days = (data_end - data_beginning).days

    for i in range(count_days + 1):
        if data_beginning + datetime.timedelta(days=i) in list_data:
            sesions_data = sesions_data + '{' + f'x: "{data_beginning + datetime.timedelta(days=i)}", y: {list_data.count(data_beginning + datetime.timedelta(days=i))}' + '},'
        else:
            sesions_data = sesions_data + '{' + f'x: "{data_beginning + datetime.timedelta(days=i)}", y: 0' + '},'
        
    list_sesions_date = []

    for item in sesions:
        if item.data >= data_beginning and item.data <= data_end:
            list_sesions_date.append(item)

    context = {
        'company': company,
        'sesions': list_sesions_date,
        'sesions_data': sesions_data,
        'data_beginning': str(data_beginning),
        'data_end': str(data_end),
        'min_data': str(list_data[-1]),
        'max_data': str(list_data[0]),
    }
    return render(request, 'redirect_links/detail_company.html', context)

def delete_company(request, id):
    Companies.objects.get(id = id).delete()
    return redirect('list_companies')