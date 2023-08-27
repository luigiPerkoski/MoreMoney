from django.shortcuts import render, HttpResponse
from .models import Extract, Money, Account

def index(request): #*Menu 

    #criar filtragem para saber qual extrato é de qual conta #!CREATE
    
    extract = Extract.objects.order_by('date') #list of object
    money = Money.objects.get(id=1) #show futuremoney
    
    context = {'extract_list': extract, 'money': money}
    return render(request, 'pages/index.html', context=context)

def accounts(request):

    account = Account.objects.order_by('name')

    context = {'account_list': account}
    return render(request, 'pages/accounts.html', context=context)