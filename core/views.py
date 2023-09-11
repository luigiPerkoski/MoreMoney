from django.shortcuts import render, redirect, HttpResponse
from .models import Extract, Money, Account
from .forms import NewExtract, NewAccount
from django import forms

#! Minhas funções para mostrar as paginas aqui

def index(request):
    #*===============================================================
    extract = Extract.objects.order_by('date') 


    #// Check se exite um objeto no modelo Money
    if len(Money.objects.order_by('name')) < 1:
        money = Money(name="Money",value=0, future_value=0, extract_profit=0, extract_damege=0)
        money.save()



    #//Calcula o total em cada conta 
    for accounts in Account.objects.order_by('name'):

        value = 0
        future_value = 0

        for object in Extract.objects.order_by('date'):
            if object.account == accounts:
                match object.type:

                    case 'P':
                        future_value += object.value

                    case 'D':
                        future_value -= object.value
            
            if object.account == accounts and object.pay:
                match object.type:

                    case 'P':
                        value += object.value

                    case 'D':
                        value -= object.value
        
        Account.objects.filter(id=accounts.id).update(future_value=future_value, value=value)


    #//Atualiza o total de dinheiro 
    money = 0
    future_money = 0

    for object in Account.objects.order_by('name'):

        future_money += object.future_value
        money += object.value

    Money.objects.update(value=money, future_value=future_money)


    #//Return
    context = {'extract_list': extract, 'money': round(money, 2), 'future_money': round(future_money, 2)}
    return render(request, 'pages/index.html', context=context)

def accounts(request):
    #*===============================================================
    account = Account.objects.order_by('name')

    #//Return
    context = {'account_list': account}
    return render(request, 'pages/accounts.html', context=context)

def damege(request):
    #*===============================================================
    damege = Extract.objects.filter(type='D')

    #// Check se exite um objeto no modelo Money
    if len(Money.objects.order_by('name')) < 1:
        money = Money(name="Money",value=0, future_value=0, extract_profit=0, extract_damege=0)
        money.save()

    #//Calcula o total de extratos negativos 
    extract_damage = 0
    
    for object in damege:
        if object.pay:
            extract_damage += object.value

    Money.objects.update(extract_damege=extract_damage)

    #//Return
    context = {'dameges': damege, 'extract_damege': extract_damage}
    return render(request, 'pages/damege.html', context=context)

def profit(request):
    #*===============================================================
    profit = Extract.objects.filter(type='P')

    #// Check se exite um objeto no modelo Money
    if len(Money.objects.order_by('name')) < 1:
        money = Money(name="Money",value=0, future_value=0, extract_profit=0, extract_damege=0)
        money.save()

    #//Calcula o total de extratos positivos  
    extract_profit = 0
    
    for object in profit:
        if object.pay:
            extract_profit += object.value

    Money.objects.update(extract_profit=extract_profit)

    #//Return
    context = {'profits': profit, 'extract_profit': extract_profit}
    return render(request, 'pages/profit.html', context=context)

def processar_formulario(request, id):
    #*===============================================================
    if request.method == 'POST':

        var = request.POST.get(f'pay_checkbox_{id}')

        if var == None:
            Extract.objects.filter(id=id).update(pay=False)
        else:
            Extract.objects.filter(id=id).update(pay=True)
        
        return redirect(index)
    
def new_extract(request):
    #*===============================================================
    forms = NewExtract()

    context = {'forms': forms}

    return render(request, 'pages/new_extract.html', context)

def extract_forms(request):
    #*===============================================================
    forms = NewExtract(request.POST)
    if forms.is_valid():
        forms.save()
        return redirect(index)

def new_account(request):
    #*===============================================================
    forms = NewAccount()

    context = {"forms": forms}

    return render (request, 'pages/new_account.html', context )

def new_extract_from_account(request, account): 
    #*===============================================================
    categoria_padrao = Account.objects.get(id=account)

    forms = NewExtract(initial={'account': categoria_padrao})


    context = {'forms': forms}

    return render(request, 'pages/new_extract.html', context)

def accounts_forms(request):
    #*=============================================================== 
    forms = NewAccount(request.POST)
    if forms.is_valid():
        forms.save()
        return redirect(index)