from django.shortcuts import render, HttpResponse
from .models import Extract, Money, Account

def index(request): #*Menu 

    #criar filtragem para saber qual extrato é de qual conta #!CREATE
    
    extract = Extract.objects.order_by('date') #list of object 
    account = Account.objects.order_by('name')
    money = Money.objects.get(id=1) #show futuremoney
    
    context = {'extract_list': extract, 'money': money, 'account': account}
    return render(request, 'pages/index.html', context=context)

