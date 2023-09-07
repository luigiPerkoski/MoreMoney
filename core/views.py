from django.shortcuts import render, redirect, HttpResponse
from .models import Extract, Money, Account
from .forms import NewExtract, NewAccount

def index(request): 
    
    extract = Extract.objects.order_by('date') 
    money = Money.objects.get(id=1) 


    money.calc_future_value()
    
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
    
def new_extract(request):

    forms = NewExtract()

    context = {'forms': forms}

    return render(request, 'pages/new_extract.html', context)

def extract_forms(request):
    forms = NewExtract(request.POST)
    if forms.is_valid():
        forms.save()
        return redirect(index)

def new_account(request):

    forms = NewAccount()

    context = {"forms": forms}

    return render (request, 'pages/new_account.html', context )

def accounts_forms(request):
    forms = NewAccount(request.POST)
    if forms.is_valid():
        forms.save()
        return redirect(index)