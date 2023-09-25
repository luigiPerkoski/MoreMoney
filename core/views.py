from django.shortcuts import render, redirect, HttpResponse
from .models import Extract, Money, Account
from .forms import NewExtract, NewAccount, SearchForm

#! Minhas funções para mostrar as paginas aqui

def index(request):
    #*===============================================================
    extract = Extract.objects.order_by('date') 
    form = SearchForm()
    response = []

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

    #//Pesquisa

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            for c in extract:
                if query.upper() in c.name.upper():
                    response.append(c)
            extract = response[:]
        else:
            extract = Extract.objects.order_by('date') 
    else:
        form = SearchForm()
        extract = Extract.objects.order_by('date') 

    #//Return
    context = {'extract_list': extract, 'money': round(money, 2), 'future_money': round(future_money, 2), 'len_extract_list':len(extract), 'form': form}
    return render(request, 'pages/index.html', context=context)

def accounts(request):
    #*===============================================================
    account = Account.objects.order_by('name')
    response = []
    #//Pesquisa

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            for c in account:
                if query.upper() in c.name.upper():
                    response.append(c)
            account = response[:]
        else:
            account = Account.objects.order_by('name') 
    else:
        form = SearchForm()
        account = Account.objects.order_by('name')

    #//Return
    context = {'account_list': account, 'form': form}
    return render(request, 'pages/accounts.html', context=context)

def damege(request):
    #*===============================================================
    damege = Extract.objects.filter(type='D')
    form = SearchForm()

    #// Check se exite um objeto no modelo Money
    if len(Money.objects.order_by('name')) < 1:
        money = Money(name="Money",value=0, future_value=0, extract_profit=0, extract_damege=0)
        money.save()

    #//Calcula o total de extratos negativos 
    extract_damage = 0
    future_extract_damage = 0
    
    for object in damege:
        if object.pay:
            extract_damage += object.value
            future_extract_damage += object.value
        else:
            future_extract_damage += object.value

    Money.objects.update(extract_damege=extract_damage)

    #//Pesquisa
    

    #//Return
    context = {'dameges': damege, 'extract_damege': extract_damage,'future_extract_damage': future_extract_damage, 'len_dameges': len(damege), 'form': form}
    return render(request, 'pages/damege.html', context=context)

def profit(request):
    #*===============================================================
    profit = Extract.objects.filter(type='P')
    form = SearchForm()

    #// Check se exite um objeto no modelo Money
    if len(Money.objects.order_by('name')) < 1:
        money = Money(name="Money",value=0, future_value=0, extract_profit=0, extract_damege=0)
        money.save()

    #//Calcula o total de extratos positivos  
    extract_profit = 0
    future_extract_profit = 0
    for object in profit:
        if object.pay:
            extract_profit += object.value
            future_extract_profit += object.value
        else:
            future_extract_profit += object.value

    Money.objects.update(extract_profit=extract_profit)

    #//Pesquisa


    #//Return
    context = {'profits': profit, 'extract_profit': extract_profit,'future_extract_profit': future_extract_profit, 'len_profits': len(profit), 'form': form}
    return render(request, 'pages/profit.html', context=context)

def processar_formulario(request, page, id):
    #*===============================================================
    if request.method == 'POST':

        var = request.POST.get(f'pay_checkbox_{id}')

        if var == None:
            Extract.objects.filter(id=id).update(pay=False)
        else:
            Extract.objects.filter(id=id).update(pay=True)
        
        return redirect(page)
    
def new_extract(request):
    #*===============================================================
    forms = NewExtract()

    accounts = Account.objects.order_by('name')

    context = {'forms': forms, "contas": accounts}

    return render(request, 'pages/new_extract.html', context)

def extract_forms(request):
    #*===============================================================
    forms = NewExtract(request.POST)
    if forms.is_valid():
        name = forms.cleaned_data['name']
        value = forms.cleaned_data['value']
        account = forms.cleaned_data['account']
        type = forms.cleaned_data['type']
        date = forms.cleaned_data['date']
        description = forms.cleaned_data['description']
        pay = forms.cleaned_data['pay']

        object = Extract(name=name, value=value, account=account, type=type, date=date, descripition=description, pay=pay)

        object.save()
        return redirect (index)

def new_account(request):
    #*===============================================================
    accounts = Account.objects.order_by('name')
    forms = NewAccount()

    context = {"contas": accounts, 'forms': forms}

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
        name = forms.cleaned_data['name']
        value = forms.cleaned_data['value']
        type = forms.cleaned_data['type']
        description = forms.cleaned_data['description']

        object = Account(name=name, value=value, type=type, descripition=description)

        object.save()
        return redirect (index)

def search_view(request):
    #*=============================================================== 
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Extract.objects.filter(name=query)
        else:
            results = []
    else:
        form = SearchForm()
        results = []
    
    context = {'form': form, 'results': results}

    return redirect('/')

def delete_extract(request, id):
    #*=============================================================== 
    post = Extract.objects.get(id=id)
    post.delete()
    return redirect('index')

def delete_account(request, id):
    #*=============================================================== 
    post = Account.objects.get(id=id)
    post.delete()
    return redirect('accounts')

def extract(request, id):

    extract = Extract.objects.get(id=id)

    forms = NewExtract(initial={'name': extract.name, 'value':extract.value, 'account': extract.account, 'type': extract.type, 'date': extract.date, 'pay': extract.pay, 'descripition': extract.descripition})


    context = {'forms': forms, 'id': id}

    return render(request, 'pages/extract.html', context)

def extract_forms_update(request, id):
    
    item = Extract.objects.get(id=id)
    if request.method == 'POST':
        form = NewExtract(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = NewExtract(initial={'name': extract.name, 'value':extract.value, 'account': extract.account, 'type': extract.type, 'date': extract.date, 'pay': extract.pay, 'descripition': extract.descripition})

    return render(request, 'extract.html', {'form': form})