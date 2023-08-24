from django.shortcuts import render, HttpResponse
from .models import Extract, Account

def index(request): #*Menu 

    #criar filtragem para saber qual extrato é de qual conta #!CREATE
    
    extract = Extract.objects.order_by('date') #list of object 
    account = Account.objects.order_by('name') #teste
    #var money

    context = {'extract_list': extract, 'account_list': account}
    return render(request, 'pages/index.html', context=context)

