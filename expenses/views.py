from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from . models import Category, Expense
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference


def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/authentication/login')
def index (request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_num = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_num)
    if UserPreference.objects.filter(user = request.user).exists():
        currency = UserPreference.objects.get(user = request.user).currency
    else:
        currency = 'INR - Indian Rupee'
    context = {
        
        'expenses':expenses,
        'page_obj':page_obj,
        'currency':currency,
        'categories':categories,
    }
    return render (request, 'expenses/index.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/authentication/login')
def add_expense (request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method =='GET':
        return render (request, 'expenses/add_expense.html', context)
    
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        if not amount:
            messages.error(request, 'Amount is required!')
            return render (request, 'expenses/add_expense.html', context)
        if not description:
            messages.error(request, 'Description is required!')
            return render (request, 'expenses/add_expense.html', context)
        if not category:
            messages.error(request, 'Category is required!')
            return render (request, 'expenses/edit_expense.html', context)
        if not date:
            messages.error(request, 'Date is required!')
            return render (request, 'expenses/edit_expense.html', context)
        
        
        
        Expense.objects.create(owner=request.user, amount=amount, date=date, category=category, description=description)
        messages.success(request, 'Expense saved successfully')
        return redirect('nexpenses')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense':expense,
        'values':expense,
        'categories':categories
    }
    
    
    if request.method=='GET':
        return render (request, 'expenses/edit_expense.html', context)
    
    
    if request.method=='POST':
        expense = Expense.objects.get(pk=id)
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        if not amount:
            messages.error(request, 'Amount is required!')
            return render (request, 'expenses/add_expense.html', context)
        if not description:
            messages.error(request, 'Description is required!')
            return render (request, 'expenses/add_expense.html', context)
        if not category:
            messages.error(request, 'Category is required!')
            return render (request, 'expenses/edit_expense.html', context)
        if not date:
            messages.error(request, 'Date is required!')
            return render (request, 'expenses/edit_expense.html', context)
        
        Expense.objects.create(owner=request.user, amount=amount, date=date, category=category, description=description)
        expense.owner=request.user
        expense.amount=amount
        expense.date=date
        expense.category=category
        expense.description=description
        expense.save()
        messages.success(request, 'Expense updated successfully!')
        return redirect('nexpenses')
    
    else:
        messages.info(request, 'Handling POST form')
        return render (request, 'expenses/edit_expense.html', context)

def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense deleted successfully! ')
    return redirect ('nexpenses')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/authentication/login')
def expense_category_summary(request):
    expenses = Expense.objects.filter(owner=request.user)
    finalrep = {}

    def get_category(expenses):
        return expenses.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)
    return JsonResponse({'expense_category_data': finalrep}, safe=False)



def stats_view(request):
    return render(request, 'expenses/e_stats.html')




