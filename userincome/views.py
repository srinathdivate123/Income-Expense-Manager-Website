from . models import Source, UserIncome
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.shortcuts import render, redirect
import json
from django.http import JsonResponse

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/authentication/login')
def index (request):
    categories = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_num = request.GET.get('page')
    page_obj = Paginator.get_page( paginator, page_num)
    if UserPreference.objects.filter(user = request.user).exists():
        currency = UserPreference.objects.get(user = request.user).currency
    else:
        currency = 'INR - Indian Rupee'
    context = {
        'income':income,
        'page_obj':page_obj,
        'currency':currency
    }
    return render (request, 'income/index.html', context)


@login_required(login_url='/authentication/login')
def add_income (request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method =='GET':
        return render (request, 'income/add_income.html', context)
    
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']
        if not amount:
            messages.error(request, 'Amount is required!')
            return render (request, 'income/add_income.html', context)
        if not description:
            messages.error(request, 'Description is required!')
            return render (request, 'income/add_income.html', context)
        if not source:
            messages.error(request, 'Source is required!')
            return render (request, 'income/add_income.html', context)
        if not date:
            messages.error(request, 'Date is required!')
            return render (request, 'income/add_income.html', context)
        UserIncome.objects.create(owner=request.user, amount=amount, date=date, source=source, description=description)
        messages.success(request, 'Income saved successfully')
        return redirect('nincome')





def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    if UserPreference.objects.filter(user = request.user).exists():
        currency = UserPreference.objects.get(user = request.user).currency
    else:
        obj = UserPreference.objects.create(user = request.user, currency = 'INR - Indian Rupee')
        currency = obj.currency
    context = {
        'income':income,
        'values':income,
        'sources':sources,
        'currency':currency
    }
    
    
    if request.method=='GET':
        return render (request, 'income/edit_income.html', context)
    
    
    if request.method=='POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']
        if not amount:
            messages.error(request, 'Amount is required!')
            return render (request, 'income/edit_income.html', context)
        if not description:
            messages.error(request, 'Description is required!')
            return render (request, 'income/edit_income.html', context)
        if not source:
            messages.error(request, 'Source is required!')
            return render (request, 'income/edit_income.html', context)
        if not date:
            messages.error(request, 'Date is required!')
            return render (request, 'income/edit_income.html', context)
        

        income.owner=request.user
        income.amount=amount
        income.date=date
        income.source=source
        income.description=description
        income.save()
        messages.success(request, 'Income updated successfully!')
        return redirect('nincome')
    
    
    
    
    else:
        messages.info(request, 'Handling POST form')
        return render (request, 'expenses/edit_expense.html', context)

def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income deleted successfully! ')
    return redirect ('nincome')




def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)




def income_source_summary(request):
    income = UserIncome.objects.filter(owner=request.user)
    finalrep = {}

    def get_source(income):
        return income.source
    source_list = list(set(map(get_source, income)))

    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = income.filter(source=source)

        for item in filtered_by_source:
            amount += item.amount
        return amount

    for x in income:
        for y in source_list:
            finalrep[y] = get_income_source_amount(y)

    return JsonResponse({'income_source_data': finalrep}, safe=False)



def stats_view(request):
    return render(request, 'income/i_stats.html')