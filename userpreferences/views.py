from pdb import Pdb
from django.shortcuts import render, redirect
import json
from django.conf import settings
from . models import UserPreference, SharePreference, GetPreference
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import json
from django.http import JsonResponse
from django.urls import reverse
import threading
from expenses.models import Expense
from userincome.models import UserIncome
import pdb

import os



def SharePreference_View(request):
    users = User.objects.all()    
    user = User.objects.filter(username=request.user)
    exists = SharePreference.objects.filter(user=request.user).exists()
    share_preferences = None
    if exists: 
        share_preferences = SharePreference.objects.get(user=request.user)
    if request.method == 'GET':
        return render(request,'preferences/advanced.html', {'users':users, 'user':user, 'share_preferences':share_preferences} )
    else:
        share_to_user = request.POST['ShowToUser']
        if exists:
            share_preferences.ShowingTo=share_to_user
            share_preferences.save()
        else:
            SharePreference.objects.create(user=request.user, ShowingTo=share_to_user)
        u = User.objects.get(username=share_to_user) 
        email = u.email
        current_site = get_current_site(request)
        email_body = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(email)),
            'uidb32': urlsafe_base64_encode(force_bytes(request.user.username))
            }

        link=reverse('nVerificationView', kwargs={'uidb64': email_body['uid'], 'uidb32':email_body['uidb32']})
        email_subject = 'View ' +request.user.username+  '\'s expenses'
        activate_url = 'https://'+current_site.domain+link
        email = EmailMessage(
            email_subject,
            'Hi '+ u.username + ', we received a request from ' + request.user.username + ' that they wanted to share their expense and income summary to you. In order to accept this request, please click the below link - \n' + activate_url,
            'noreply@semycolon.com',
            [email],
        )
        EmailThread(email).start()
        messages.success(request, 'User ' + u.username + ' will now be able to see a summary of your expenses and income!' )
        return render(request,'preferences/advanced.html', {'users':users, 'user':user,'share_preferences':share_preferences} )


def VerificationView(request, uidb64, uidb32):
    try:
        email = force_str(urlsafe_base64_decode(uidb64))   #Email of U2
        sent_by_username = force_str(urlsafe_base64_decode(uidb32)) #Username u1
    except Exception as ex:
        messages.error(request, 'There was some problem with the link that you just clicked. Please request for a new link!')
        return redirect('nlogin')
    user_receiving_data = User.objects.get(email=email) #User u2
    username_receiving_data = user_receiving_data.username #Username u2
    exists = GetPreference.objects.filter(user=user_receiving_data).exists()
    if exists:
        sent_by_username = GetPreference.objects.get(user=user_receiving_data).SeeingFrom
    else:
        GetPreference.objects.create(user=user_receiving_data, SeeingFrom=sent_by_username)
    
    messages.success(request, 'Welcome '+user_receiving_data.username+', you may now login to view the expense summary of '+sent_by_username+'!')
    return redirect('nlogin')


def expense_category_summary(request):
    sent_by_username = GetPreference.objects.get(user=request.user).SeeingFrom
    if sent_by_username:
        user = User.objects.get(username=sent_by_username)
    else:
        user=SharePreference.objects.get(username=sent_by_username)
    expenses = Expense.objects.filter(owner=user)
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

def income_source_summary(request):
    sent_by_username = GetPreference.objects.get(user=request.user).SeeingFrom
    if sent_by_username:
        user = User.objects.get(username=sent_by_username)
    else:
        user=SharePreference.objects.get(username=sent_by_username)
    income = UserIncome.objects.filter(owner=user)
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





def ViewOthersSummary(request):
    exists = GetPreference.objects.filter(user=request.user).exists()
    if exists:
        sent_by_username = GetPreference.objects.get(user=request.user).SeeingFrom
    else:
        sent_by_username = None
    return render (request, 'others/viewothers.html',{'sent_by_username':sent_by_username})










class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)



def index(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(file_path, 'r') as json_file:
        # Converting JSON file into a python dictionary
        data = json.load(json_file)
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})
            
    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists: 
        user_preferences = UserPreference.objects.get(user=request.user)
    if request.method =='GET':
        return render(request, 'preferences/index.html',{'currencies':currency_data, 'user_preferences':user_preferences})
       
    else:
        currency = request.POST['currency']
        if exists:
            user_preferences.currency=currency
            user_preferences.save()
        else:
            UserPreference.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved successfully!' )
        return render (request, 'preferences/index.html',{'currencies':currency_data,'user_preferences':user_preferences})


