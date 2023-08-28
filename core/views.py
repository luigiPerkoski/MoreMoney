from django.shortcuts import render, redirect
from .models import Extract, Money, Account

def index(request): 

    #criar filtragem para saber qual extrato é de qual conta #!CREATE
    
    extract = Extract.objects.order_by('date') #list of object
    money = Money.objects.get(id=1) #show futuremoney
    
    context = {'extract_list': extract, 'money': money}
    return render(request, 'pages/index.html', context=context)

def accounts(request):

    account = Account.objects.order_by('name')

    context = {'account_list': account}
    return render(request, 'pages/accounts.html', context=context)

def damege(request):

    damege = Extract.objects.filter(type='D')
    money = Money.objects.get(id=1)

    context = {'extract_damege': damege, 'money': money}
    return render(request, 'pages/damege.html', context=context)

def profit(request):

    profit = Extract.objects.filter(type='P')
    money = Money.objects.get(id=1)

    context = {'extract_profit': profit, 'money': money}
    return render(request, 'pages/profit.html', context=context)

def processar_formulario(request, id):

    if request.method == 'POST':

        var = request.POST.get(f'pay_checkbox_{id}')

        if var == None:
            Extract.objects.filter(id=id).update(pay=False)
        else:
            Extract.objects.filter(id=id).update(pay=True)
        
        return redirect(index)